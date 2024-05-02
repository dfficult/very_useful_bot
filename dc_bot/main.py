import discord
from discord.ext import commands
from eat import *
from vub_math import *
from money import *
from yazy import *
from others import *

TOKEN = "TOKEN"  # 換成你的TOKEN
PREFIX = "!"

# Create bot instance
bot = commands.Bot(command_prefix=PREFIX,intents=discord.Intents.all())

@bot.event
async def on_ready():
    slash = await bot.tree.sync()
    print(f"已登入：{bot.user}")
    print(f"已載入 {len(slash)} 個指令")
    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=""))
    # await bot.change_presence(activity=discord.Game(name="Grand Theft Auto VI"))
    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Never Gonna Give You Up"))


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content == "hello world":
        await message.channel.send("Hello World!")
    
# Commands
@bot.command()
async def vubhelp(ctx):
    await ctx.send("https://www.github.com/dfficult/very_useful_bot")

@bot.command()
async def change_status(ctx, *type, **status):
    match type:
        case "watch":
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status))
        case "game":
            await bot.change_presence(activity=discord.Game(name=status))
        case "listen":
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status))
    await ctx.send(f"Changed to [{type}] [{status}]")


bot.tree.add_command(which_day_next_sun)
bot.tree.add_command(eat)
bot.tree.add_command(addfood)

bot.tree.add_command(gowhere)

bot.tree.add_command(simfrac)
bot.tree.add_command(rand)
bot.tree.add_command(dice)
bot.tree.add_command(vector)
bot.tree.add_command(surface)
bot.tree.add_command(average)
bot.tree.add_command(det3)
bot.tree.add_command(det2)
bot.tree.add_command(p)
bot.tree.add_command(c)

bot.tree.add_command(mborrow)
bot.tree.add_command(mhistory)
bot.tree.add_command(mdelete)

bot.tree.add_command(yazystart)
bot.tree.add_command(yazyreset)
bot.tree.add_command(yazyroll)
bot.tree.add_command(yazyhold)
bot.tree.add_command(yazychoose)
bot.tree.add_command(yazyscore)


# Run
bot.run(TOKEN)