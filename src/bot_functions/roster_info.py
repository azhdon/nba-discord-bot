import requests
import discord
from IDS import team_ids

def get_roster(team, season):
    # Capitalize the team name for consistency
    team = team.capitalize()

    # Headers for the HTTP request
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'x-nba-stats-token': 'true',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X04_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.394530 Safari/537.36',
        'x-nba-stats-origin': 'stats',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Referer': 'https://stats.nba.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    # Get the team ID for the specified team
    team_id = team_ids.get(team)

    # Return an error message if team ID is not found
    if not team_id:
        return f"No team ID found for {team}", None 

    # Construct the URL to fetch the team roster
    url = f"https://stats.nba.com/stats/commonteamroster?LeagueID=&Season={season}&TeamID={team_id}"

    # Send the HTTP request to fetch the team roster
    response = requests.get(url, headers=headers)
    roster = response.json()

    # Create the player names string
    player_names = '```ini\n'
    for player in roster["resultSets"][0]["rowSet"]:
        player_jersey = player[6]
        player_name = player[3]
        player_pos = player[7]
        player_names += f"{player_jersey} {player_name} ({player_pos})\n"
    player_names += "```"

    return player_names
