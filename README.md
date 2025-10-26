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

# Add Canadian flag for Canadian teams
python process_schedule.py --canada

# Display as calendar view instead of bulleted list
python process_schedule.py --calendar

# Combine options
python process_schedule.py --highlight "Winnipeg Jets" --star "Montreal Canadiens" --weekend --canada --calendar
```

## Output

The script generates:
- `europe-friendly-games.md` - Markdown file with filtered games
- Console output with the same content

Games are filtered to show only those starting between 13:00-22:00 Paris time, making them suitable for European viewers.

### Display Formats

By default, games are displayed as a bulleted list. Use the `--calendar` flag to display games in a monthly calendar view using markdown tables.

### Formatting

- **Bold text** - Games highlighted with `--highlight` or `--star`
- **⭐ Star symbol** - Games highlighted with `--star`
- *Italic text* - Games on Friday or Saturday (Paris time) when using `--weekend`
- **🇨🇦 Canadian flag** - Games with Canadian teams when using `--canada`
