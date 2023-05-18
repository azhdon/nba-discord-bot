# Import necessary modules
import discord
import datetime
import json
import requests

def get_player_info(message, season = 2022):
    # Split the user's input message into their first and last name
    user_first_name, user_last_name = message.split(" ")[0],  message.split(" ")[1]
    # Query the API to get a list of players matching the given first and last names
    url = requests.get(f'https://www.balldontlie.io/api/v1/players?search={user_first_name}+{user_last_name}')
    players = url.json()
        
    if len(players["data"]) > 0:
        # Get the first player from the list of players returned by the API
        player = players["data"][0]
        player_id = player["id"]
        team = player["team"]["full_name"]
        team_name = player["team"]["name"]
        # Query the API to get the player's stats for the given season
        url = f"https://www.balldontlie.io/api/v1/season_averages?season={season}&player_ids[]={player_id}"
        stats = requests.get(url)
        season_stats = stats.json()["data"]
        if season_stats:
            # Convert the stats data to a nested list
            stats_list = []
            for row in season_stats:
                stats_list.append([row["pts"],row["ast"],row["reb"]])
                stats_list.append([row["stl"],row["blk"],row["turnover"]])
                stats_list.append([row["fg_pct"],row["fg3_pct"],row["ft_pct"]])

            # Round the values to one decimal place
            for i in range(0, len(stats_list)):
                    for j in range(0, len(stats_list)):
                        stats_list[i][j] = round(stats_list[i][j], 1)
            # Generate a formatted string from the nested list
            fg_pct = stats_list[2][0]
            threeP_pct = stats_list[2][1]
            ft_pct = stats_list[2][2]
            formatted_fg_pct = "{:.2f}".format(fg_pct).lstrip('0')
            formatted_three_pct = "{:.2f}".format(threeP_pct).lstrip('0')
            formatted_ft_pct = "{:.2f}".format(ft_pct).lstrip('0')
            stats_text = f"PTS:{stats_list[0][0]} | STL:{stats_list[1][0]} | FG%:{formatted_fg_pct}\n"
            stats_text += f"AST:{stats_list[0][1]}  | BLK:{stats_list[1][1]} | 3P%:{formatted_three_pct}\n"
            stats_text += f"REB:{stats_list[0][2]}  | TOV:{stats_list[1][2]} | FT%:{formatted_ft_pct}"
            # Construct a formatted string containing the player's name, team, and stats
            player_text = f"```{player['first_name']} {player['last_name']} | {team}\n\n"
            player_text += f"{stats_text}```"

    # Return the formatted string containing the player's name, team, and stats
    return player_text