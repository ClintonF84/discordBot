import os
import json
import discord
import datetime
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Get the Discord token from .env
TOKEN = os.getenv("DISCORD_TOKEN")


def loadJson():
    with open('games.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def saveJson(data):
    with open('games.json', 'w') as f:
        json.dump(data, f, indent=4) 

# Load the configuration from config.json
with open("config.json", "r", encoding='utf-8') as config_file:
    config = json.load(config_file)

WELCOME_MESSAGE = config["welcome_message"]
WELCOME_CHANNEL_ID = config["welcome_channel_id"]
POLL_QUESTIONS = config["games"]
REACTION_OPTIONS = config["reaction_options"]

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
@bot.command()
async def poll(ctx):
    for question in POLL_QUESTIONS:
        message = await ctx.send(f"**{question}**")
        for reaction in REACTION_OPTIONS:
            await message.add_reaction(reaction)


@bot.command(name='addGame')
async def AddGame(ctx, game: str):
    data = loadJson()
    existingGames = data['games']
    gameObject =json.load(game)
    existingGames.append(gameObject)
    saveJson(existingGames)

@bot.command(name='updateGame')
async def UpdateGame(ctx, gameName: str):
    data = loadJson()
    gameToUpdate = data['games'].get(gameName, {})
    gameToUpdate.playedDate = datetime.today().date()
    saveJson(gameToUpdate)


# Run the bot
bot.run(TOKEN)
