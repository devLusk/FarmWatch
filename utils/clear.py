async def clear_webhook_messages(channel):
    deleted = 0

    async for msg in channel.history(limit=200):
        if msg.webhook_id is not None:
            await msg.delete()
            deleted += 1

    print(f">>> Deleted {deleted} webhook messages")