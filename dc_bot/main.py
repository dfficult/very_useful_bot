# VeryUsefulBot v1.5.1
# 2025.1.22


# --- Settings ---
TOKEN = "TOKEN"

# === main.py ===
import discord, datetime, asyncio
from discord.ext import commands, tasks
try:
    from eat import *
    from vub_math import *
    from money import *
    from dates import *
    from codes import *
    from notice import *
    from flashcard import *
    from calculator import *
except Exception as e:
    print(e)
    print("Try running 'main.py' again in the '/dc_bot' directory")
    input("Press Enter to exit ...")
    exit()


# --- Discord bot token ---
if TOKEN == "TOKEN":
    x = input("Token is not specified, enter your token or leave it blank to exit: ")
    if x == '': exit()
    else: TOKEN = x


# --- Create bot instance ---
bot = commands.Bot(command_prefix="!",intents=discord.Intents.all())


# --- Bot loop ---
@tasks.loop(minutes=1)
async def notice_loop():
    result = check_notice()
    if result:
        for i in result:
            # result = [..., [user, channel, embed], ...]
            channel = bot.get_channel(i[1])
            await channel.send(f"<@{i[0]}>",embed=i[2])


# --- Sync bot loop ---
async def sync_task_to_minute():
    now = datetime.datetime.now()
    # Calculate the time to wait until the next minute starts
    seconds_to_wait = 60 - now.second
    await asyncio.sleep(seconds_to_wait)
    notice_loop.start()


# --- Load bot ---
@bot.event
async def on_ready():
    slash = await bot.tree.sync()
    print(f"{bot.user} 已成功登入，並已載入{len(slash)}個指令")
    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="YouTube"))
    await bot.change_presence(activity=discord.Game(name="Grand Theft Auto VI"))
    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Never Gonna Give You Up"))
    await sync_task_to_minute()



# --- Actions when bot receives any message ---
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content == "hello world":
        await message.channel.send("Hello World!")
    

# --- An example command ---
@app_commands.command(name="vubhelp", description="所有指令說明")
async def vubhelp(interaction: discord.Interaction):
    embed = discord.Embed(
        title="歡迎使用 VeryUsefulBot",
        description="前往指令列表 ➡️ https://www.github.com/dfficult/very_useful_bot"
    )
    await interaction.response.send_message(embed=embed)


# --- Add all commands to the bot ---
bot.tree.add_command(vubhelp)
# notice.py
bot.tree.add_command(notice)
bot.tree.add_command(delnotice)
# code.py
bot.tree.add_command(code)
bot.tree.add_command(submit_code)
bot.tree.add_command(new_code_q)
# dates.py
bot.tree.add_command(today)
bot.tree.add_command(daysleft)
# eat.py
bot.tree.add_command(eat)
bot.tree.add_command(addfood)
# vub_math.py
bot.tree.add_command(correlation)
bot.tree.add_command(simfrac)
bot.tree.add_command(factorize)
bot.tree.add_command(solve21)
bot.tree.add_command(solve31)
bot.tree.add_command(rand)
bot.tree.add_command(dice)
bot.tree.add_command(vector)
bot.tree.add_command(vectorl)
bot.tree.add_command(surface)
bot.tree.add_command(average)
bot.tree.add_command(det3)
bot.tree.add_command(det2)
bot.tree.add_command(invrmtx2)
bot.tree.add_command(p)
bot.tree.add_command(c)
# money.py
bot.tree.add_command(mlend)
bot.tree.add_command(mhistory)
bot.tree.add_command(mdelete)
# flashcard.py
bot.tree.add_command(flashcard)
# calculator.py
bot.tree.add_command(calculator)


# Run the bot
bot.run(TOKEN)
