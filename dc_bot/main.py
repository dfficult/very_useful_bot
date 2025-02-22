import discord, datetime, asyncio
from discord.ext import commands, tasks
try:
    from eat import *
    from vub_math import *
    from money import *
    from dates import *
    from oj import *
    from notice import *
    from flashcard import *
    from calculator import *
    from wordle import *
except FileNotFoundError as e:
    print(f"Error: Wrong Directory {e}")
    print("  Please run 'main.py' in the '/dc_bot' directory")
    print("  To do so, simply enter 'cd dc_bot' after pressing [Enter] to exit\n")
    input("Press [Enter] to exit ...")
    exit()


# --- Token ---
with open("token.txt", "r") as f: token = f.readline()
if token == "":
    entered = input("Token not found, please enter your token or press [Enter] to exit: ")
    if entered == '':
        exit()
    else:
        print(f"You entered: {entered}")
        confirm = input(f"Are you sure you want to use this token? [y/n] ")
        if turn_lower_to_upper(confirm) == 'Y':
            token = entered
            with open("token.txt", 'w') as f: f.write(token)
        else:
            exit()


# --- Create bot instance ---
bot = commands.Bot(command_prefix="!",intents=discord.Intents.all())


# --- Bot loop ---
# Notice.py
@tasks.loop(minutes=1)
async def notice_loop():
    result = check_notice()
    if result:
        for i in result:
            # result = [..., [user, channel, embed], ...]
            channel = bot.get_channel(i[1])
            await channel.send(f"<@{i[0]}>",embed=i[2])
# Sync bot loop
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
    await bot.change_presence(activity=discord.Game(name="Wordle"))
    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Never Gonna Give You Up"))
    await sync_task_to_minute()


# --- Bot Events ---
# Normal message reply
# Easter eggs
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content == "hello world":
        await message.channel.send("Hello World!")



# --- Help command ---
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
bot.tree.add_command(notice_after)
bot.tree.add_command(notice_at)
bot.tree.add_command(notice_delete)
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
# wordle.py
bot.tree.add_command(wordle)


# Run the bot
bot.run(token)
