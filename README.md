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
