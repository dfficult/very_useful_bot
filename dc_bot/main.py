import discord, datetime, asyncio
from discord.ext import commands, tasks
try:
    from eat import *
    from vub_math import *
    from dates import *
    from oj import *
    from notice import *
    from flashcard import *
    from calculator import *
    from wordle import *
    from text_edit import *
    from expenses import *
    import settings, user_options
except FileNotFoundError as e:
    print(text("bot.err",e))
    print(text("bot.wrong_dir.description"))
    input(text("bot.enter_to_exit"))
    exit()


# --- Token ---
with open("token.txt", "r") as f: token = f.readline()
if token == "":
    entered = input(text("bot.token_notfound"))
    if entered == '':
        exit()
    else:
        print(text("bot.token_entered",entered))
        confirm = input(text("bot.token_confirm"))
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
    print(text("bot.login",bot.user,len(slash)))
    await bot.change_presence(activity=settings.Activity.playing)
    await sync_task_to_minute()


# --- Bot Events ---
# Normal message reply
# Easter eggs
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content == "hello world":
        await message.channel.send(text("bot.helloworld"))



# --- Help command ---
@app_commands.command(name="help", description=text("cmd.help.description"))
async def vubhelp(interaction: discord.Interaction):
    embed = discord.Embed(
        title=text("cmd.help.title"),
        description=text("cmd.help.text")
    )
    await interaction.response.send_message(embed=embed)


# --- Add all commands to the bot ---
bot.tree.add_command(vubhelp)
bot.tree.add_command(user_options.option)
# notice.py
bot.tree.add_command(notice_after)
bot.tree.add_command(notice_at)
bot.tree.add_command(notice_delete)
bot.tree.add_command(note_list)
bot.tree.add_command(sticky_note)
# code.py
bot.tree.add_command(code)
bot.tree.add_command(submit_code)
# dates.py
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
bot.tree.add_command(common_deg_to_rad)
# flashcard.py
bot.tree.add_command(flashcard)
# calculator.py
bot.tree.add_command(calculator)
bot.tree.add_command(calculate)
# wordle.py
bot.tree.add_command(wordle)
bot.tree.add_command(wordle_context_menu)
# text_edit.py
bot.tree.add_command(wordcount)
# expenses.py
bot.tree.add_command(m_new_record)
bot.tree.add_command(m_wallet)

# Run the bot
bot.run(token)
