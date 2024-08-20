import os
import json
import discord
import subprocess
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime
from game import Game  # Import the Game class

# Load environment variables from .env file
load_dotenv()

# Get the Discord token from .env
TOKEN = os.getenv("DISCORD_TOKEN")

REACTION_OPTIONS = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫']  # Custom reactions

def load_games():
    with open("games.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        return [Game(**game) for game in data["games"]]

def save_games(games):
    with open("games.json", "w", encoding="utf-8") as f:
        json.dump({"games": [game.to_dict() for game in games]}, f, indent=4)

def get_unplayed_games(limit=4):
    games = load_games()
    return [game for game in games if not game.played_date][:limit]

def update_game_votes(game_name):
    games = load_games()
    for game in games:
        if game.name.lower() == game_name.lower():
            game.vote()
            break
    save_games(games)

# Load the configuration from config.json
with open("config.json", "r", encoding="utf-8") as config_file:
    config = json.load(config_file)

WELCOME_MESSAGE = config["welcome_message"]
WELCOME_CHANNEL_ID = config["welcome_channel_id"]

# Set up the bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        await channel.send(WELCOME_MESSAGE.format(member=member.mention))

@bot.command(name="poll")
async def poll(ctx):
    games = get_unplayed_games(len(REACTION_OPTIONS))  # Limit options based on available reactions
    if not games:
        await ctx.send("No unplayed games available for voting.")
        return

    description = "\n".join([f"{REACTION_OPTIONS[idx]}: {game.name} [How To Play]({game.how_to_link})" for idx, game in enumerate(games)])
    poll_message = await ctx.send(f"**Vote for a game by reacting:**\n{description}", suppress_embeds=True)

    for idx in range(len(games)):
        await poll_message.add_reaction(REACTION_OPTIONS[idx])

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return

    message = reaction.message
    if not message.content.startswith("**Vote for a game by reacting:**"):
        return

    games = get_unplayed_games(len(REACTION_OPTIONS))
    if not games:
        return

    # Map reactions to game names
    reaction_to_game = {REACTION_OPTIONS[idx]: game.name for idx, game in enumerate(games)}

    selected_game_name = reaction_to_game.get(reaction.emoji)
    if selected_game_name:
        update_game_votes(selected_game_name)
        await message.channel.send(f"{user.mention} voted for {selected_game_name}!")

@bot.command(name="addGame")
async def add_game(ctx, game_name: str, how_to_link: str):
    games = load_games()
    new_game = Game(game_name, how_to_link)
    games.append(new_game)
    save_games(games)

@bot.command(name="clear")
async def clear_games(ctx):
    save_games([])

@bot.command(name="updateCode")
async def update_code(ctx):
    subprocess.run(["git", "pull", "origin", "main"], check=True)

bot.run(TOKEN)
