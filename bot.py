import os

from config import load_config

import discord
from discord.ext import commands

token, intents = load_config()

bot = commands.Bot(command_prefix="!", intents=intents)

# ======== EVENTS ========

@bot.event
async def on_ready():
    print(f"Bot has been connected as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.webhook_id is None:
        return
    
    embed = message.embeds[0]
    print("Embed title:", embed.title)
    print("Embed description:", embed.description)

    if embed.image and embed.image.url:
        print("Embed image:", embed.image.url)

    await bot.process_commands(message)

# ======== RUN ========

bot.run(token)