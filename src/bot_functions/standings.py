from basketball_reference_scraper.seasons import get_standings
from IDS import emoji_ids
def get_standings1():
    standings_dict = get_standings()
    # Initialize empty string variable
    standings_str = ""

    # Extract the Western Conference standings from the dictionary
    western_standings = standings_dict['WESTERN_CONF']
    standings_str += "\n\nWestern Conference\n\n"

    # Extract the team name, wins, and losses for each team in the Western Conference
    count = 1
    for index, row in western_standings.iterrows():
        team = row['TEAM']
        team_name = team.split(" ")[-1]
        if team_name[-1] == "*":
            team_name = team_name[0:-1:]
            team = team[0:-1]
        emoji = f"<:{team_name}:{emoji_ids[team_name]}>"
        wins = row['W']
        losses = row['L']

        # Append team name and win-loss record to string with new line character
        if count < 10:
            standings_str += f"`{count}  |`{emoji}`{team} | {wins}-{losses}`\n"
        else:
            standings_str += f"`{count} |`{emoji}`{team} | {wins}-{losses}`\n"
        count += 1

    # Extract the Eastern Conference standings from the dictionary
    eastern_standings = standings_dict['EASTERN_CONF']

    standings_str += "\nEastern Conference\n\n"
    # Extract the team name, wins, and losses for each team in the Eastern Conference
    count = 1
    for index, row in eastern_standings.iterrows():
        team = row['TEAM']
        team_name = team.split(" ")[-1]
        if team_name[-1] == "*":
            team_name = team_name[0:-1:]
            team = team[0:-1]
        emoji = f"<:{team_name}:{emoji_ids[team_name]}>"
        wins = row['W']
        losses = row['L']

        # Append team name and win-loss record to string with new line character
        if count < 10:
            standings_str += f"`{count}  |`{emoji}`{team} | {wins}-{losses}`\n"
        else:
            standings_str += f"`{count} |`{emoji}`{team} | {wins}-{losses}`\n"
        count += 1

    # Return the standings string, removing the trailing new line character
    return standings_str
