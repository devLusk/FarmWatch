import discord
from services.poll import setup_prompt_embed, setup_complete_embed, setup_disapproval_embed

async def setup(ctx):
    await ctx.message.delete()

    poll_message = await ctx.send(embed=setup_prompt_embed())
    
    await poll_message.add_reaction("✅")
    await poll_message.add_reaction("❌")

    def check(reaction, user):
        return (
            user == ctx.author and
            reaction.emoji in ["✅", "❌"] and 
            reaction.message.id == poll_message.id
        )

    reaction, user = await ctx.bot.wait_for('reaction_add', check=check)

    await poll_message.clear_reactions()
    
    if reaction.emoji == "✅":
        await poll_message.edit(embed=discord.Embed(description="Creating channels... ⏳"))
        
        webhook_channel = await ctx.guild.create_text_channel(name="farm-webhook")
        summary_channel = await ctx.guild.create_text_channel(name="farm-summary")

        new_channel_webhook = await webhook_channel.create_webhook(name="Farm Bot Webhook")
      
        await poll_message.edit(embed=setup_complete_embed(webhook_channel.mention, summary_channel.mention, new_channel_webhook.url), delete_after=60)
        
    else: 
        await poll_message.edit(embed=discord.Embed(description="Creating webhook... ⏳"))

        current_channel_webhook = await ctx.channel.create_webhook(name="Farm Bot Webhook")

        await poll_message.edit(embed=setup_disapproval_embed(ctx.channel.mention, current_channel_webhook.url), delete_after=60)