#!/usr/bin/env python3
import csv
import argparse
from datetime import datetime
from zoneinfo import ZoneInfo
import calendar

def parse_and_filter_schedule(highlighted_teams=None, starred_teams=None, mark_weekend=False, mark_canada=False):
    """Process NHL schedule and find Europe-friendly game times."""

    if highlighted_teams is None:
        highlighted_teams = []
    if starred_teams is None:
        starred_teams = []

    # Canadian NHL teams
    canadian_teams = ['Winnipeg Jets', 'Toronto Maple Leafs', 'Montreal Canadiens',
                      'Ottawa Senators', 'Calgary Flames', 'Edmonton Oilers', 'Vancouver Canucks']

    europe_friendly_games = []

    with open('nhl-schedule.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)  # Skip header row

        for row in reader:
            if len(row) < 6:
                continue

            # Extract columns A, C, D, F (indices 0, 2, 3, 5)
            date_str = row[0].strip()  # Column A: Date
            time_str = row[2].strip()  # Column C: Time in New York
            away_team = row[3].strip()  # Column D: Away team
            home_team = row[5].strip()  # Column F: Home team

            # Skip empty or invalid rows
            if not date_str or not time_str or not away_team or not home_team:
                continue

            try:
                # Parse date and time in New York timezone
                datetime_str = f"{date_str} {time_str}"
                ny_time = datetime.strptime(datetime_str, "%m/%d/%Y %I:%M %p")
                ny_time = ny_time.replace(tzinfo=ZoneInfo("America/New_York"))

                # Convert to Paris time
                paris_time = ny_time.astimezone(ZoneInfo("Europe/Paris"))

                # Filter games starting at or before 22:00 Paris time
                # Include games from 13:00 (1 PM) to 22:00 (10 PM) Paris time
                # This captures:
                # - European games (which show as early in NYC but normal time in Paris)
                # - Early afternoon games in North America (which are evening in Paris)
                paris_hour = paris_time.hour
                paris_minute = paris_time.minute

                # Include games from 13:00 through 22:00 Paris time
                if 13 <= paris_hour <= 22:
                    # Check if any highlighted team is playing
                    is_highlighted = any(
                        team.lower() in away_team.lower() or team.lower() in home_team.lower()
                        for team in highlighted_teams
                    )

                    # Check if any starred team is playing
                    is_starred = any(
                        team.lower() in away_team.lower() or team.lower() in home_team.lower()
                        for team in starred_teams
                    )

                    # Check if game is on Friday (4) or Saturday (5) and weekend marking is enabled
                    is_weekend = mark_weekend and paris_time.weekday() in [4, 5]

                    # Check if any Canadian team is playing and marking is enabled
                    is_canadian = mark_canada and any(
                        team in away_team or team in home_team
                        for team in canadian_teams
                    )

                    europe_friendly_games.append({
                        'date': paris_time.strftime('%Y-%m-%d'),
                        'time': paris_time.strftime('%H:%M'),
                        'ny_time': ny_time.strftime('%H:%M'),  # For debugging
                        'away_team': away_team,
                        'home_team': home_team,
                        'is_highlighted': is_highlighted,
                        'is_starred': is_starred,
                        'is_weekend': is_weekend,
                        'is_canadian': is_canadian,
                        'datetime': paris_time  # Store full datetime for calendar formatting
                    })

            except (ValueError, IndexError) as e:
                # Skip rows with parsing errors
                continue

    return europe_friendly_games

def format_game_text(game, include_date=True):
    """Format a single game with all its decorations (stars, flags, italics, bold).

    Args:
        game: Game dictionary with all metadata
        include_date: Whether to include the date in the output (default True)

    Returns:
        Formatted game text string
    """
    # Build the base game text
    if include_date:
        game_text = f"{game['date']} at {game['time']} - {game['away_team']} @ {game['home_team']}"
    else:
        game_text = f"{game['time']} - {game['away_team']} @ {game['home_team']}"

    # Build prefix with star and/or Canadian flag
    prefix = ""
    if game['is_starred']:
        prefix = "⭐ "
    if game['is_canadian']:
        prefix += "🇨🇦 "

    # Apply italics for weekend games
    if game['is_weekend']:
        game_text = f"*{game_text}*"

    # Apply bold for starred or highlighted games
    if game['is_starred'] or game['is_highlighted']:
        return f"**{prefix}{game_text}**"
    else:
        return f"{prefix}{game_text}"

def format_as_markdown(games, highlighted_teams=None, starred_teams=None):
    """Format the games list as Markdown with highlighted and starred teams."""

    if highlighted_teams is None:
        highlighted_teams = []
    if starred_teams is None:
        starred_teams = []

    if not games:
        return "# Europe-Friendly NHL Games (2025/2026)\n\nNo games found starting at or before 22:00 Paris time."

    md = "# Europe-Friendly NHL Games (2025/2026)\n\n"
    md += f"*Games starting at or before 22:00 Paris time (all times in 24-hour format)*\n\n"
    md += f"**Total games found: {len(games)}**\n\n"

    # Count highlighted games
    highlighted_games = [g for g in games if g['is_highlighted']]
    if highlighted_games and highlighted_teams:
        team_list = ', '.join(highlighted_teams)
        md += f"**{team_list} games (highlighted): {len(highlighted_games)}**\n\n"

    # Count starred games
    starred_games = [g for g in games if g['is_starred']]
    if starred_games and starred_teams:
        team_list = ', '.join(starred_teams)
        md += f"**{team_list} games (starred): {len(starred_games)}**\n\n"

    md += "---\n\n"

    for game in games:
        formatted_game = format_game_text(game, include_date=True)
        md += f"- {formatted_game}\n"

    return md

def format_as_calendar(games, highlighted_teams=None, starred_teams=None):
    """Format the games list as a monthly calendar view using markdown tables."""

    if highlighted_teams is None:
        highlighted_teams = []
    if starred_teams is None:
        starred_teams = []

    if not games:
        return "# Europe-Friendly NHL Games (2025/2026)\n\nNo games found starting at or before 22:00 Paris time."

    md = "# Europe-Friendly NHL Games (2025/2026)\n\n"
    md += f"*Games starting at or before 22:00 Paris time (all times in 24-hour format)*\n\n"
    md += f"**Total games found: {len(games)}**\n\n"

    # Count highlighted games
    highlighted_games = [g for g in games if g['is_highlighted']]
    if highlighted_games and highlighted_teams:
        team_list = ', '.join(highlighted_teams)
        md += f"**{team_list} games (highlighted): {len(highlighted_games)}**\n\n"

    # Count starred games
    starred_games = [g for g in games if g['is_starred']]
    if starred_games and starred_teams:
        team_list = ', '.join(starred_teams)
        md += f"**{team_list} games (starred): {len(starred_games)}**\n\n"

    md += "---\n\n"

    # Group games by year-month
    from collections import defaultdict
    games_by_month = defaultdict(list)

    for game in games:
        dt = game['datetime']
        year_month = (dt.year, dt.month)
        games_by_month[year_month].append(game)

    # Sort months chronologically
    sorted_months = sorted(games_by_month.keys())

    # Create a calendar for each month
    for year, month in sorted_months:
        month_name = calendar.month_name[month]
        md += f"## {month_name} {year}\n\n"

        # Create calendar header (Mon-Sun)
        md += "| Mon | Tue | Wed | Thu | Fri | Sat | Sun |\n"
        md += "|-----|-----|-----|-----|-----|-----|-----|\n"

        # Get the calendar for this month
        cal = calendar.monthcalendar(year, month)

        # Create a dict of games by day
        games_by_day = defaultdict(list)
        for game in games_by_month[(year, month)]:
            day = game['datetime'].day
            games_by_day[day].append(game)

        # Build the calendar rows
        for week in cal:
            row_parts = []
            for day in week:
                if day == 0:
                    # Empty cell for days not in this month
                    row_parts.append("")
                else:
                    # Check if there are games on this day
                    day_games = games_by_day.get(day, [])
                    if day_games:
                        # Format the cell with game info
                        cell = f"**{day}**<br><br>"
                        for game in day_games:
                            formatted_game = format_game_text(game, include_date=False)
                            cell += formatted_game + "<br>"
                        row_parts.append(cell.rstrip("<br>"))
                    else:
                        # Just the day number
                        row_parts.append(str(day))

            md += "| " + " | ".join(row_parts) + " |\n"

        md += "\n"

    return md

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Process NHL schedule and find Europe-friendly game times.'
    )
    parser.add_argument(
        '--highlight',
        type=str,
        default='',
        help='Comma-separated list of teams to highlight in bold (e.g., "Winnipeg Jets,Toronto Maple Leafs")'
    )
    parser.add_argument(
        '--star',
        type=str,
        default='',
        help='Comma-separated list of teams to highlight with star symbol (e.g., "Montreal Canadiens")'
    )
    parser.add_argument(
        '--weekend',
        action='store_true',
        help='Italicize games on Friday or Saturday (Paris time)'
    )
    parser.add_argument(
        '--canada',
        action='store_true',
        help='Add Canadian flag emoji for games with Canadian teams'
    )
    parser.add_argument(
        '--calendar',
        action='store_true',
        help='Display games in a calendar view using markdown tables instead of a bulleted list'
    )

    args = parser.parse_args()

    # Parse teams from comma-separated strings
    highlighted_teams = [team.strip() for team in args.highlight.split(',') if team.strip()]
    starred_teams = [team.strip() for team in args.star.split(',') if team.strip()]

    games = parse_and_filter_schedule(highlighted_teams, starred_teams, args.weekend, args.canada)

    # Choose formatting based on --calendar flag
    if args.calendar:
        markdown_output = format_as_calendar(games, highlighted_teams, starred_teams)
    else:
        markdown_output = format_as_markdown(games, highlighted_teams, starred_teams)

    # Write to file
    with open('europe-friendly-games.md', 'w', encoding='utf-8') as f:
        f.write(markdown_output)

    print(markdown_output)
