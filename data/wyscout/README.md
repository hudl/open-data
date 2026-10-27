# Hudl Wyscout Open Data

Event and tracking data from Hudl Wyscout for a selection of matches.

> **Status:** work in progress. The event files are available. The tracking files are not published yet.

## Matches

Five matches from the Croatian top division, the SuperSport HNL (Wyscout competition `302`), season 2025/26 (Wyscout season `191645`).

| Match ID | Date | Home | Away | Score |
|---|---|---|---|---|
| 5716532 | 2025-09-13 | Rijeka | Lokomotiva Zagreb | 1–1 |
| 5716531 | 2025-09-14 | Osijek | Vukovar | 4–0 |
| 5716536 | 2025-09-20 | Hajduk Split | Dinamo Zagreb | 0–2 |
| 5716540 | 2025-09-28 | Dinamo Zagreb | Slaven Belupo | 4–1 |
| 5716546 | 2025-10-03 | Istra 1961 | Varaždin | 1–0 |

All IDs are Wyscout IDs. They are not the same as the IDs in the StatsBomb data elsewhere in this repository.

## Data

| Path | Contents |
|---|---|
| `events/<match_id>.json` | Events for each match. Each file is named for a Wyscout match ID. |
| `tracking/<match_id>.jsonl` | Tracking data for each match, one frame per line. Each file is named for a Wyscout match ID. |

### Events

The event files are exported from the Wyscout API v4 (`matches/<match_id>/events`) with tag details. Each file contains:

* `events`: every event in the match.
* `match`: the match details.
* `teams`: the two teams.
* `players`: the players in the match.
* `meta`: metadata about the response.

The Wyscout API documentation describes the format:

* [Events overview](https://apidocs.wyscout.com/?version=4#tag/Events/Overview): the event model, with event [types](https://apidocs.wyscout.com/?version=4#tag/Events/Overview/Types), [locations](https://apidocs.wyscout.com/?version=4#tag/Events/Overview/Location), [possessions](https://apidocs.wyscout.com/?version=4#tag/Events/Overview/Possession-specific-data) and the data for each event type, for example [passes](https://apidocs.wyscout.com/?version=4#tag/Events/Overview/Pass) and [shots](https://apidocs.wyscout.com/?version=4#tag/Events/Overview/Shot).
* [`GET /matches/{wyId}/events`](https://apidocs.wyscout.com/?version=4#tag/Events/paths/~1matches~1%7BwyId%7D~1events/get): the endpoint and its response schema.

### Tracking

The tracking data for each match is generated from the match video with the latest Hudl tracking model. The format will be documented when the data is published.

In the Wyscout API, tracking is available from [`GET /matches/{wyId}/fulltracking`](https://apidocs.wyscout.com/?version=4#tag/Tracking/paths/~1matches~1%7BwyId%7D~1fulltracking/get), which returns a link to download the tracking file.
