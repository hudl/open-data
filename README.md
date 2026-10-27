# Hudl Open Data

Welcome to the Hudl Open Data repository.

Hudl shares football data publicly to enhance understanding of the game. We want to actively encourage new research and analysis at all levels. Therefore we have made data from some of our products freely available for public use for research projects and genuine interest in football analytics.

Data from each product is kept separately, as each product has its own data format and its own IDs for competitions, matches, teams and players.

## Hudl StatsBomb

### Terms & Conditions

If you publish, share or distribute any research, analysis or insights based on this data, please state the data source as StatsBomb and use our logo, available in our [Media Pack](https://statsbomb.com/media-pack/).

### Getting Started

The data is provided as JSON files exported from the StatsBomb Data API, in the following structure:

| Path | Contents | Documentation |
|---|---|---|
| [`data/competitions.json`](./data/competitions.json) | All available competitions and seasons. | [Competitions v2.0.0](./doc/Open%20Data%20Competitions%20v2.0.0.pdf) |
| [`data/matches/<competition_id>/<season_id>.json`](./data/matches/) | Matches for each competition and season. Each folder is named for a competition ID, and each file is named for a season ID within that competition. | [Matches v3.0.0](./doc/Open%20Data%20Matches%20v3.0.0.pdf) |
| [`data/events/<match_id>.json`](./data/events/) | Events for each match. Each file is named for a match ID. | [Events v4.0.0](./doc/Open%20Data%20Events%20v4.0.0.pdf) |
| [`data/lineups/<match_id>.json`](./data/lineups/) | Lineups for each match. Each file is named for a match ID. | [Lineups v2.0.0](./doc/Open%20Data%20Lineups%20v2.0.0.pdf) |
| [`data/three-sixty/<match_id>.json`](./data/three-sixty/) | StatsBomb 360 freeze frames for selected matches. Each file is named for a match ID. | [360 Frames v1.0.0](./doc/Open%20Data%20360%20Frames%20v1.0.0%20%281%29.pdf) |

To find the data for a match, look up the competition and season in `competitions.json`, then find the match in the matching file in `matches`. Use its `match_id` to open the files in `events`, `lineups` and `three-sixty`.

The [StatsBomb Open Data Specification v1.1](./doc/StatsBomb%20Open%20Data%20Specification%20v1.1.pdf) gives an overview of all data types, event types and pitch coordinates.

## Downloading only some of the data

The full repository is large (the StatsBomb data alone is about 15 GB). If you need data from only one product, use a partial clone with a sparse checkout. Git then downloads only the files in the folders that you choose.

You need Git 2.27 or later.

### Wyscout data only

```sh
git clone --depth 1 --filter=blob:none --sparse https://github.com/hudl/open-data.git
cd open-data
git sparse-checkout set data/wyscout
```

### StatsBomb data only

This includes all the StatsBomb folders and leaves out `data/wyscout`:

```sh
git clone --depth 1 --filter=blob:none --sparse https://github.com/hudl/open-data.git
cd open-data
git sparse-checkout set data/events data/lineups data/matches data/three-sixty
```

### Notes

* The files at the top level of the repository and directly in `data/` (for example `data/competitions.json`) are always included.
* `--depth 1` downloads only the latest version. Remove it if you need the history.
* To change the folders later, run `git sparse-checkout set` again with the new list. Git downloads the files that are missing.
* To get all the data, run `git sparse-checkout disable`.
