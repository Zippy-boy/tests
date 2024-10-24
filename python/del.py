import discord

TOKEN = "MTE4NzAwNDA3NzA1ODU3MjMyOA.GesLi3" + ".MCoxEmnV-JqbeFVVQCiyvJoyf3mbWntnTLfyzg"
GUILD_ID = 1297901498805518337  # Replace with your guild ID

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
