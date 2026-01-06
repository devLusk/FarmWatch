import discord

def setup_prompt_embed():
    return discord.Embed(
        title="🐝 Farm Bot Setup",
        description=(
            "To keep your server organized, it’s recommended to use separate channels:\n\n"
            "• **#farm-webhook** — Real-time farm notifications\n"
            "• **#farm-summary** — Session summaries and reports\n\n"
            "How would you like to proceed?\n"
            "✅ Create the channels automatically\n"
            "❌ Use this channel for everything"
        ),
        color=0xF2C94C
    )


def setup_complete_embed(webhook_channel, summary_channel, webhook_url):
    return discord.Embed(
        title="✅ Setup Complete",
        description=(
            "Your server has been successfully configured.\n\n"
            f"• {webhook_channel} — Webhook notifications\n"
            f"• {summary_channel} — Summaries and reports\n\n"
            "To enable webhook integration in **NatroMacro**:\n"
            "1. Open NatroMacro settings\n"
            "2. Go to the Discord webhook section\n"
            "3. Paste the webhook URL below\n"
            "4. Enable **Startup Report** and **Hourly Report**\n\n"
            f"```{webhook_url}```"
        ),
        color=0x2ECC71
    )


def setup_disapproval_embed(channel_mention, webhook_url):
    return discord.Embed(
        title="✅ Setup Complete",
        description=(
            f"All farm notifications will be sent in {channel_mention}.\n\n"
            "To enable webhook integration in **NatroMacro**:\n"
            "1. Open NatroMacro settings\n"
            "2. Go to the Discord webhook section\n"
            "3. Paste the webhook URL below\n"
            "4. Enable **Startup Report** and **Hourly Report**\n\n"
            f"```{webhook_url}```"
        ),
        color=0x2ECC71
    )