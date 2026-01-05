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

# ======== HELPERS ========

def strip_timestamp(text: str):
    if not text:
        return ""

    if "] " in text:
        return text.split("] ", 1)[1]

    return text


def extract_current_honey(description: str):
    if not description:
        return None

    lines = description.split("\n")
    for line in lines:
        if "Current Honey:" in line:
            return line.split(":", 1)[1].strip()

    return None

# ======== EVENTS ========

@bot.event
async def on_ready():
    print(f"🐝 {bot.user.name} is ready")
    print(f"📊 Status: Monitoring farm sessions")


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

    raw_title = embed.title or ""
    raw_description = embed.description or ""

    title = strip_timestamp(raw_title)
    description = strip_timestamp(raw_description)

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
    
    # ======== STARTUP REPORT ========
    if title == "Startup Report":
        initial_honey = extract_current_honey(description)
        print(f">>> Startup Report | Initial Honey: {initial_honey}")
        return
    
    # ======== HOURLY REPORT ========
    if title == "Hourly Report":
        hourly_reports_count += 1
        print(f">>> Hourly Report #{hourly_reports_count}")

        if embed.image and embed.image.url:
            last_hourly_image_url = embed.image.url
            print(">>> Hourly image saved")

        return

    # ======== END: MACRO ========
    if "End: Macro" in description:
        session_end_time = message.created_at
        session_active = False

        print(">>> Macro ended")
        print("Initial Honey:", initial_honey)
        print("Hourly Reports:", hourly_reports_count)
        print("Last Hourly Image:", last_hourly_image_url)

        return

    await bot.process_commands(message)


# ======== RUN ========

bot.run(token)