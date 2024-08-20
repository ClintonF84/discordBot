import os
import json
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the Discord token from .env
TOKEN = os.getenv("DISCORD_TOKEN")
# test
print('token ->' + TOKEN)
# Load the configuration from config.json
print("Current working directory:", os.getcwd())
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

# Run the bot
bot.run(TOKEN)
