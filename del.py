import discord

TOKEN = "MTExNTIwMjU0MzQxNzU2MTE1OQ.GvSXnq.kzE73fkf8iEk6YFPDNJhuJvJXIJKheJQc2LEhY"  # Replace with your bot token
GUILD_ID = 1115241407628705833  # Replace with your guild ID

intents = discord.Intents.default()
intents.guilds = True
# intents.channels = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Bot connected as {client.user}")

    # Get the guild
    guild = client.get_guild(GUILD_ID)
    if guild is None:
        print("Guild not found")
        await client.close()
        return

    # Delete all channels
    for channel in guild.channels:
        await channel.delete()
        print(f"Channel deleted: {channel.name}")

    print("All channels deleted")
    await client.close()

# Run the bot
client.run(TOKEN)
