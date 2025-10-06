import discord
from discord.ext import commands
import json, os
from dotenv import load_dotenv

DATA_FILE = "scoreboard.json"

def load_scoreboard():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_scoreboard():
    with open(DATA_FILE, "w") as f:
        json.dump(scoreboard, f, indent=4)

load_dotenv()

TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True  # Required for commands to work
bot = commands.Bot(command_prefix="!", intents=intents)

scoreboard = load_scoreboard()

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command()
async def save(ctx):
    save_scoreboard()
    await ctx.send("💾 Scoreboard saved!")

def render_table():
    if not scoreboard:
        return "No players yet!"
   
    header = f"{'Rank':<5}{'Name':<15}{'Wins':<6}{'Losses':<8}{'Ties':<6}\n"
    rows = []
    sorted_board = sorted(scoreboard, key=lambda x: x['wins'], reverse=True)
    for i, player in enumerate(sorted_board, start=1):
        rows.append(f"{i:<5}{player['name']:<15}{player['wins']:<6}{player['losses']:<8}{player['ties']:<6}")
    return "```\n" + header + "\n".join(rows) + "\n```"

@bot.command()
async def add(ctx, name: str):
    if any(p['name'].lower() == name.lower() for p in scoreboard):
        await ctx.send(f"{name} is already on the scoreboard!")
        return
    scoreboard.append({"name": name, "wins": 0, "losses": 0, "ties": 0})
    await ctx.send(f"✅ Added {name} to the scoreboard.")

@bot.command()
async def update(ctx, name: str, wins: int = 0, losses: int = 0, ties: int = 0):
    for player in scoreboard:
        if player['name'].lower() == name.lower():
            player['wins'] += wins
            player['losses'] += losses
            player['ties'] += ties
            await ctx.send(f"Updated {name}!")
            return
    await ctx.send(f"❌ Player {name} not found.")

@bot.command(name="scoreboard")
async def scoreboard_cmd(ctx):
    await ctx.send(render_table())

bot.run(TOKEN)