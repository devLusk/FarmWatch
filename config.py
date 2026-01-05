import os

import discord
from dotenv import load_dotenv

def load_config():

    load_dotenv()

    token = os.getenv("DISCORD_TOKEN")

    intents = discord.Intents.default()
    intents.message_content = True

    return token, intents