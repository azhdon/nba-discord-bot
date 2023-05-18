import discord
import os
from dotenv import load_dotenv
from IDS import emoji_ids, team_ids
from datetime import datetime
from bot_functions.game_schedule import get_game_schedule
from bot_functions.standings import get_standings1
from bot_functions.player_info import get_player_info
from bot_functions.roster_info import get_roster
from bot_functions.league_leaders import get_league_leaders
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option

client = discord.Client()

load_dotenv()

token = os.environ['DISCORD_TOKEN']

slash = SlashCommand(client, sync_commands=True)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@slash.slash(name="games",
             description="Get the Scores and Schedule for Upcoming and Current NBA Games.")
async def games(ctx: SlashContext):
    game_text = get_game_schedule()
    embed = discord.Embed(
        description=game_text,
        color=discord.Color.blue()
    )
    now = datetime.now()  
    formatted_date = now.strftime("%B %d %Y")  
    embed.set_author(name=f"NBA Games for {formatted_date}")
    await ctx.send(embed=embed)


@slash.slash(name="standings",
             description="Get the current NBA standings.")
async def standings(ctx: SlashContext):
    standings_text = get_standings1()
    embed = discord.Embed(
        description=standings_text,
        color=discord.Color.blue()
    )
    embed.set_author(name="Current Stadnings for the NBA")
    await ctx.send(embed=embed)
 
@slash.slash(name="player",
             description="Get information about an NBA player.",
             options=[
                 create_option(
                     name="name",
                     description="The Name of the Player.",
                     option_type=3,
                     required=True
                 ),
                 create_option(
                     name="season",
                     description="The Season | Example 2022 | Optional",
                     option_type=3,
                     required=False
                 )
             ])
async def player(ctx: SlashContext, name: str, season: str="2022"):
    player_info_text = get_player_info(name, season)
    embed = discord.Embed(
        description=player_info_text,
        color=discord.Color.blue()
    )
    embed.set_author(name=f"{name} Per Game Stats \n{season} Season")
    await ctx.send(embed=embed)


@slash.slash(name="roster",
             description="Displays the roster for a given team and season",
             options=[
                 create_option(
                     name="team",
                     description="The Name of the Team",
                     option_type=3,
                     required=True
                 ),
                 create_option(
                     name="season",
                     description="The Season | Example (2022)",
                     option_type=3,
                     required=True
                 )
             ])
async def display_roster(ctx, team: str, season: str):
    roster = get_roster(team, season)
    file = discord.File(f"logos\{team_ids.get(team)}.png", filename="thumbnail.png")
    embed = discord.Embed(description=roster)
    embed.set_author(name=f"Roster for the {season} {team.capitalize()}")
    embed.set_thumbnail(url="attachment://thumbnail.png")
    await ctx.send(embed=embed, file=file)

@slash.slash(name="league-leaders",
             description="Get the current NBA standings.",
             options=[
                 create_option(
                     name="season",
                     description="The Season | Example: 2022",
                     option_type=3,
                     required=True
                 ),
                 create_option(
                     name="stat",
                     description="The Stat You Want To See | Example: PTS, REB, AST ",
                     option_type=3,
                     required=True
                 ),
                  create_option(
                     name="players",
                     description="The Amount Of Players You Want To See | Example (15) | Optional",
                     option_type=3,
                     required=False
                 )
             ])
async def leagueLeaders(ctx: SlashContext, season: str, stat: str, players: str=10):
    guild = ctx.guild
    season_convert = int(season[2:5]) + 1
    if int(season) < 2009 and int(season) >= 2000:
        season = season + "-0" + str(season_convert)
    elif int(season) == 1999:
        season = "1999-00"
    else:   
        season = season + "-" + str(season_convert)
    standings_text = get_league_leaders(season, stat, players)
    embed = discord.Embed(
        description=standings_text,
        color=discord.Color.blue()
    )
    statpg = stat[0].capitalize()
    season_convert = season[0:4]
    embed.set_author(name=f'{statpg}PG League Leaders for {season_convert} Season')
    await ctx.send(embed=embed)

client.run(token)

