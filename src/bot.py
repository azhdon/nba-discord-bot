from nba_api.stats.endpoints import leagueleaders
import discord
from IDS import team_ids, emoji_ids


def get_league_leaders(season, stat,count=10):
    team_ids1 = {v: k for k, v in team_ids.items()}
    stat = stat.upper()
    players = leagueleaders.LeagueLeaders('00', 'PerGame', 'S', season, 'Regular Season', stat).get_dict()
    result_text = ""
    counter = 0
    players_headers = players['resultSet']['headers']
    stat_index = players_headers.index(stat)
    for player in players['resultSet']['rowSet']:
        team_id = str(player[3])
        team_name = team_ids1[team_id]
        emoji_id = emoji_ids[team_name]
        emoji = f"<:{team_name}:{emoji_id}>"
        result_text += f"`{player[4]}`{emoji}`|{player[2]} | {player[stat_index]} {stat}`\n"
        counter += 1
        if count == counter: break

    return result_text
