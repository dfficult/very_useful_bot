import discord, datetime, asyncio, random
from discord.ext import commands, tasks
import os

import settings
from lang import text




# Token
with open("token.txt", "r") as f: token = f.readline()
if token == "":
    entered = input(text("bot.token_notfound"))
    if entered == '':
        exit()
    else:
        print(text("bot.token_entered",entered))
        confirm = input(text("bot.token_confirm"))
        if confirm.upper() == 'Y':
            token = entered
            with open("token.txt", 'w') as f: f.write(token)
        else:
            exit()


# Create bot instance
bot = commands.Bot(command_prefix="!",intents=discord.Intents.all())


# Load bot
@bot.event
async def on_ready():
    # Load cogs
    loaded_commands = 0
    loaded_failed = 0
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(text("bot.cog_loaded", filename))
                loaded_commands += 1
            except Exception as e:
                print(text("bot.cog_load_error", filename, e))
                loaded_failed += 1
    print(text("bot.cogs_load_count", loaded_commands, loaded_failed))
    # Sync Commands
    try:
        synced = await bot.tree.sync()
        print(text("bot.commands_synced", len(synced)))
    except Exception as e:
        print(text("bot.commands_sync_error", e))
    # Logged in successfully
    print(text("bot.login", bot.user.name))
    # Set bot status
    match settings.Activity.doing:
        case "watching":
            activity = discord.Activity(type=discord.ActivityType.watching, name=settings.Activity.content)
            await bot.change_presence(activity=activity)
        case "playing":
            activity = discord.Game(name=settings.Activity.content)
            await bot.change_presence(activity=activity)
        case "listening":
            activity = activity=discord.Activity(type=discord.ActivityType.listening, name=settings.Activity.content)
            await bot.change_presence(activity=activity)
        case _:
            pass
    


# Easter eggs
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content == "hello world":
        await message.channel.send(text("bot.helloworld"))




# Run the bot
bot.run(token)