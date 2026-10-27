"""Thin, temporary wrapper around the Wyscout v4 API for pulling open data.

Standard library only. Credentials are read from CLIENT_ID / CLIENT_SECRET in the
environment, or from a .env file at the repo root (which is git-ignored).

    python3 tools/wyscout_api.py get competitions areaId=HRV
    python3 tools/wyscout_api.py get competitions/<competition_id>/seasons
    python3 tools/wyscout_api.py get seasons/<season_id>/matches
    python3 tools/wyscout_api.py check <match_id> [<match_id> ...]
    python3 tools/wyscout_api.py clip <match_id> <out.mp4> [--minute 10] [--length 30]
    python3 tools/wyscout_api.py events <match_id> data/wyscout/events/<match_id>.json
    python3 tools/wyscout_api.py tracking <match_id> data/wyscout/tracking/<match_id>.jsonl
"""

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

BASE_URL = "https://apirest.wyscout.com/v4/"
TIMEOUT_SECONDS = 30
REPO_ROOT = Path(__file__).resolve().parent.parent


def _load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        # the environment wins over the file
        os.environ.setdefault(key.strip(), value.strip().strip("\"'"))


def _auth_header() -> dict[str, str]:
    _load_env_file(REPO_ROOT / ".env")
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    if not client_id or not client_secret:
        sys.exit("CLIENT_ID and CLIENT_SECRET must be set, in the environment or in .env")
    token = base64.b64encode(f"{client_id}:{client_secret}".encode("ascii")).decode("ascii")
    return {"Authorization": f"Basic {token}"}


def get(path: str, params: dict[str, str] | None = None) -> dict:
    url = BASE_URL + path.lstrip("/")
    if params:
        url += "?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(url, headers=_auth_header())
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            return json.load(response)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GET {path} failed with {e.code}: {body}") from None


def get_match_events(match_id: int) -> dict:
    return get(
        f"matches/{match_id}/events",
        {"details": "tag", "fetch": "teams,players,match"},
    )


def download_tracking(match_id: int, out: Path) -> Path:
    # the download link is signed and expires within a day, so always ask for a fresh one
    response = get(f"matches/{match_id}/fulltracking")
    url = response.get("trackingDownloadUrl")
    if not url:
        raise RuntimeError(f"No tracking available for match {match_id}: {response}")
    out.parent.mkdir(parents=True, exist_ok=True)
    partial = out.with_suffix(out.suffix + ".partial")
    with urllib.request.urlopen(url, timeout=60) as r, open(partial, "wb") as f:
        while chunk := r.read(1 << 20):
            f.write(chunk)
    partial.rename(out)
    return out


def download_clip(match_id: int, out: Path, minute: int = 10, length: int = 30) -> Path:
    """Download a short clip starting `minute` minutes into the first half."""
    offsets = get(f"videos/{match_id}", {"start": "0", "end": "1"})["offsets"]
    start = offsets["1H"]["start"] + minute * 60
    response = get(
        f"videos/{match_id}",
        {"start": str(start), "end": str(start + length), "quality": "hd"},
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(response["hd"]["url"], timeout=60) as r, open(out, "wb") as f:
        while chunk := r.read(1 << 20):
            f.write(chunk)
    return out


def check_match(match_id: int) -> None:
    """Print whether a match has events and tracking, without downloading the tracking file."""
    m = get(f"matches/{match_id}")
    print(f"{match_id}: {m.get('label')} | {m.get('dateutc')} | competition {m.get('competitionId')}"
          f" season {m.get('seasonId')} | {m.get('status')}")
    try:
        print(f"  events: {len(get_match_events(match_id).get('events', []))}")
    except RuntimeError as e:
        print(f"  events: unavailable ({e})")
    try:
        url = get(f"matches/{match_id}/fulltracking")["trackingDownloadUrl"]
        # the signed link refuses HEAD, so ask for one byte and read the total size
        request = urllib.request.Request(url, headers={"Range": "bytes=0-0"})
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as r:
            size = int(r.headers["Content-Range"].split("/")[-1])
        print(f"  tracking: {size / 1e6:.1f} MB")
    except (RuntimeError, KeyError, urllib.error.URLError) as e:
        print(f"  tracking: unavailable ({e})")


def _write_json(data: dict, out: Path | None) -> None:
    text = json.dumps(data, indent=2, ensure_ascii=False)
    if out is None:
        print(text)
        return
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text + "\n")
    print(f"wrote {out}", file=sys.stderr)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)

    p_get = sub.add_parser("get", help="GET any endpoint and print the JSON")
    p_get.add_argument("path", help="e.g. competitions/123/seasons")
    p_get.add_argument("params", nargs="*", help="query parameters as key=value")
    p_get.add_argument("-o", "--out", type=Path, help="write to a file instead of stdout")

    p_events = sub.add_parser("events", help="fetch the events for a match")
    p_events.add_argument("match_id", type=int)
    p_events.add_argument("out", type=Path, nargs="?")

    p_tracking = sub.add_parser("tracking", help="download the full tracking file for a match")
    p_tracking.add_argument("match_id", type=int)
    p_tracking.add_argument("out", type=Path)

    p_check = sub.add_parser("check", help="check matches have events and tracking")
    p_check.add_argument("match_ids", type=int, nargs="+")

    p_clip = sub.add_parser("clip", help="download a short video clip from the first half")
    p_clip.add_argument("match_id", type=int)
    p_clip.add_argument("out", type=Path)
    p_clip.add_argument("--minute", type=int, default=10, help="minutes into the first half")
    p_clip.add_argument("--length", type=int, default=30, help="clip length in seconds")

    args = parser.parse_args()
    if args.command == "clip":
        path = download_clip(args.match_id, args.out, args.minute, args.length)
        print(f"wrote {path}", file=sys.stderr)
    elif args.command == "check":
        for match_id in args.match_ids:
            check_match(match_id)
    elif args.command == "get":
        params = dict(p.split("=", 1) for p in args.params)
        _write_json(get(args.path, params), args.out)
    elif args.command == "events":
        _write_json(get_match_events(args.match_id), args.out)
    elif args.command == "tracking":
        print(f"wrote {download_tracking(args.match_id, args.out)}", file=sys.stderr)


if __name__ == "__main__":
    main()
