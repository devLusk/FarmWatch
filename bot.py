from config import load_config
from state.session import new_session, reset_session, end_session
from services.summary import build_summary
from utils.text import strip_timestamp, extract_current_honey
from utils.clear import clear_webhook_messages
from utils import commands as bot_commands
from discord.ext import commands

token, intents = load_config()
bot = commands.Bot(command_prefix="!", intents=intents)

session = new_session()

# ======== EVENTS ========

@bot.event
async def on_ready():
    print(f"🐝 Bot: {bot.user.name} (ID: {bot.user})")
    print(f"📡 Latency: {round(bot.latency * 1000)}ms")
    print("✅ Status: Monitoring farm sessions")


@bot.event
async def on_message(message):
    await bot.process_commands(message)

    if message.author == bot.user:
        return
    
    if message.webhook_id is None:
        return
    
    if not message.embeds:
        return
    
    embed = message.embeds[0]
    title = strip_timestamp(embed.title or "")
    description = strip_timestamp(embed.description or "")

    # ======== BEGIN: MAIN LOOP ========
    if  description == "Begin: Main Loop":
        reset_session(session, message.created_at)
        print(">>> Macro started")
        return

    if not session["active"]:
        return
    
    # ======== STARTUP REPORT ========
    if title == "Startup Report":
        session["initial_honey"] = extract_current_honey(description)
        print(f">>> Startup Report | Initial Honey: {session['initial_honey']}")
        return
    
    # ======== HOURLY REPORT ========
    if title == "Hourly Report":
        session["hourly_reports"] += 1
        print(f">>> Hourly Report #{session['hourly_reports']}")

        if embed.image and embed.image.url:
            session["last_hourly_image"] = embed.image.url
            print(">>> Hourly image saved")

        return

    # ======== END: MACRO ========
    if  description == "End: Macro":
        end_session(session, message.created_at)

        print(">>> Macro ended")
        print(f"Initial Honey: {session['initial_honey']}")
        print(f"Hourly Reports: {session['hourly_reports']}")
        print(f"Last Hourly Image: {session['last_hourly_image']}")


        summary = build_summary(session)
        await clear_webhook_messages(message.channel)

        await message.channel.send(summary)
        if session["last_hourly_image"]:
            await message.channel.send(session["last_hourly_image"])

        return


# ======== COMMANDS ========

@bot.command()
async def setup(ctx):
    await bot_commands.setup(ctx)


# ======== RUN ========

bot.run(token)