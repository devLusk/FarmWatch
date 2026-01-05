import os

from config import load_config

import discord
from discord.ext import commands

token, intents = load_config()

bot = commands.Bot(command_prefix="!", intents=intents)

# ======== FARM SESSION STATE ========

session_active = False
session_start_time = None
session_end_time = None

initial_honey = None

hourly_reports_count = 0
last_hourly_image_url = None

# ======== EVENTS ========

@bot.event
async def on_ready():
    print(f"Bot has been connected as {bot.user}")


@bot.event
async def on_message(message):
    global session_active
    global session_start_time, session_end_time
    global initial_honey
    global hourly_reports_count
    global last_hourly_image_url

    if message.author == bot.user:
        return
    
    if message.webhook_id is None:
        return
    
    embed = message.embeds[0]

    title = embed.title or ""
    description = embed.description or ""

    # ======== BEGIN: MAIN LOOP ========
    if "Begin: Main Loop" in description:
        print(">>> Macro started")

        session_active = True
        session_start_time = message.created_at

        # reset state
        initial_honey = None
        hourly_reports_count = 0
        last_hourly_image_url = None

        return

    if not session_active:
        return

    await bot.process_commands(message)


# ======== RUN ========

bot.run(token)