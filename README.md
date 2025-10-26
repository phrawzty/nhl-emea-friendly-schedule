# NHL Europe-Friendly Schedule

A Python script that filters NHL games to find Europe-friendly viewing times (games starting at or before 22:00 Paris time).

## Requirements

- Python 3.9+
- `nhl-schedule.csv` file (see below)

## Getting the Schedule Data

Download the NHL schedule CSV from:
https://shanemcd.org/2025/07/17/2025-26-nhl-schedule-and-results-in-excel-xlsx-and-csv-formats/

Place the `nhl-schedule.csv` file in the same directory as the script.

## Usage

```bash
# Basic usage (no teams highlighted)
python process_schedule.py

# Highlight specific teams in bold
python process_schedule.py --highlight "Winnipeg Jets,Toronto Maple Leafs"

# Highlight teams with star symbol
python process_schedule.py --star "Montreal Canadiens"

# Italicize weekend games (Friday/Saturday in Paris time)
python process_schedule.py --weekend

# Combine options
python process_schedule.py --highlight "Winnipeg Jets" --star "Montreal Canadiens" --weekend
```

## Output

The script generates:
- `europe-friendly-games.md` - Markdown file with filtered games
- Console output with the same content

Games are filtered to show only those starting between 13:00-22:00 Paris time, making them suitable for European viewers.

### Formatting

- **Bold text** - Games highlighted with `--highlight` or `--star`
- **⭐ Star symbol** - Games highlighted with `--star`
- *Italic text* - Games on Friday or Saturday (Paris time) when using `--weekend`
