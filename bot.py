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
    
    # DEBUG: show in terminal
    print("Message received from webhook:")
    print(message.content)

    if message.attachments:
        for attachment in message.attachments:
            print(f"Attachment detected: {attachment.url}")

    await bot.process_commands(message)

# ======== RUN ========

bot.run(token)