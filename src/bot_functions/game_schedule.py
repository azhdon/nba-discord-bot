import requests
import datetime
import discord
from IDS import team_ids, emoji_ids

def get_game_schedule():
    
    # Get the current date
    url = 'https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json'
    response = requests.get(url)
    games = response.json()
    response_str = ''

    # Iterate through each game in the scoreboard
    for game in games['scoreboard']['games']:
        game_status = game['gameStatus']
        away_team_name = game['awayTeam']["teamName"]
        home_team_name = game['homeTeam']["teamName"]
        
        # Replace long team name with a shorter version
        if home_team_name == "Trail Blazers":
            home_team_name = "Blazers"
        
        # Get the emojis for the home and away teams
        home_emoji = f"<:{home_team_name}:{emoji_ids[home_team_name]}>"
        away_emoji = f"<:{away_team_name}:{emoji_ids[away_team_name]}>"
        
        # Check the game status
        if game_status == 2:
            # Game is in progress
            response_str += f"{away_emoji} `{game['awayTeam']['teamTricode']} {game['awayTeam']['score']}` @ "
            response_str += f"{home_emoji} `{game['homeTeam']['score']} {game['homeTeam']['teamTricode']} | {game['gameStatusText']}`\n\n"
        elif game_status == 3:
            # Game is finished
            response_str += f"`({game['awayTeam']['wins']}-{game['awayTeam']['losses']})` {away_emoji} `{game['awayTeam']['teamTricode']} {game['awayTeam']['score']} @ {game['homeTeam']['score']}` {home_emoji} `{game['homeTeam']['teamTricode']} ({game['homeTeam']['wins']}-{game['homeTeam']['losses']}) | {game['gameStatusText']}`\n\n"
        else:
            # Game is upcoming
            response_str += f"{away_emoji} `{game['awayTeam']['teamTricode']} ({game['awayTeam']['wins']}-{game['awayTeam']['losses']})` @ "
            response_str += f"`{game['homeTeam']['teamTricode']}` {home_emoji} `({game['homeTeam']['wins']}-{game['homeTeam']['losses']}) | {game['gameStatusText']}`\n\n"
        
    return response_str
