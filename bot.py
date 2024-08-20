import os
import json
import discord
import datetime
import subprocess

from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Get the Discord token from .env
TOKEN = os.getenv("DISCORD_TOKEN")


def loadJson():
    with open("games.json", "r", encoding="utf-8") as f:
        return json.load(f)

def saveJson(data):
    with open("games.json", "w") as f:
        json.dump(data, f, indent=4) 

def GetUnplayed4Games():
    games = loadJson()
    gamesArray = games["games"]
    unplaygames = []

    count = 0
    for game in gamesArray:
        if game.get("playedDate", "") == "":
            unplaygames.append(game)
            count = count + 1
        
        if count == 4:
            break
    

    



# Load the configuration from config.json
with open("config.json", "r", encoding="utf-8") as config_file:
    config = json.load(config_file)

WELCOME_MESSAGE = config["welcome_message"]
WELCOME_CHANNEL_ID = config["welcome_channel_id"]
REACTION_OPTIONS = config["reaction_options"]
gamesdata = loadJson()

print(gamesdata)

# Set up the bot
intents = discord.Intents.default()  # Start with default intents
intents.message_content = True  # Enable message content intent if needed
intents.members = True  # Enable guild members intent if needed
intents.presences = True  # Enable presence intent if needed

bot = commands.Bot(command_prefix="!", intents=intents)

# Event to welcome new members
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        await channel.send(WELCOME_MESSAGE.format(member=member.mention))

# Command to start a poll with multiple questions
@bot.command(name="poll")
async def poll(ctx):
    for question in GetUnplayed4Games():
        message = await ctx.send(f"**{question}**")
        for reaction in REACTION_OPTIONS:
            await message.add_reaction(reaction)


@bot.command(name="addGame")
async def AddGame(ctx, gameName: str, howToLink: str):
    existingGames = gamesdata["games"]
    gameObject = {"name": gameName, "createdDate": datetime.today().date().isoformat(), "playedDate": "", "howToLink": howToLink}
    existingGames.append(gameObject)

    print(gameObject)

    saveJson({"games": existingGames})

@bot.command(name="updateGame")
async def UpdateGame(ctx, gameName: str):
    gameToUpdate = gamesdata['games'].get(gameName, {})
    gameToUpdate.playedDate = datetime.today().date().isoformat()

    saveJson(gameToUpdate)

@bot.command(name="clear")
async def clearGames(ctx):
    clear = {"games": []}
    saveJson(clear)

# this will pull latest from Main branch
@bot.command(name="updateCode")
async def updateCode(ctx):
    subprocess.run(["git", "pull", "origin", "main"], check=True)

# Run the bot
bot.run(TOKEN)
