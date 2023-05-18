# Import necessary modules
from nba_api.stats.endpoints import leagueleaders
import discord
from IDS import team_ids, emoji_ids

# Define function to get league leaders
def get_league_leaders(season, stat, count=10):
    # Reverse team IDs dictionary to get team names
    team_ids1 = {v: k for k, v in team_ids.items()}
    # Convert stat to uppercase to match API parameters
    stat = stat.upper()
    # Retrieve league leaders data from NBA API
    players = leagueleaders.LeagueLeaders('00', 'PerGame', 'S', season, 'Regular Season', stat).get_dict()
    # Initialize variable to store result text
    result_text = ""
    # Initialize counter to keep track of number of players
    counter = 0
    # Get headers from players data
    players_headers = players['resultSet']['headers']
    # Get index of desired stat in headers list
    stat_index = players_headers.index(stat)
    # Loop through each player's data
    for player in players['resultSet']['rowSet']:
        # Get team ID and use reverse dictionary to get team name
        team_id = str(player[3])
        team_name = team_ids1[team_id]
        # Get corresponding emoji ID from team name
        emoji_id = emoji_ids[team_name]
        # Format emoji with team name and ID
        emoji = f"<:{team_name}:{emoji_id}>"
        # Format player's name, team name, and stat value into result text
        result_text += f"`{player[4]}`{emoji}`|{player[2]} | {player[stat_index]} {stat}`\n"
        # Increment counter
        counter += 1
        # Exit loop if desired number of players has been reached
        if count == counter:
            break
    
    # Return result text
    return result_text