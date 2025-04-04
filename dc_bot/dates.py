# === dates.py ===
import discord
from discord import app_commands
from discord.app_commands import Choice
import datetime
from lang import *

# --- Check if it's a leap year ---
def is_leap(year: int) -> bool:
    if ((year % 4 == 0) and (year % 100 != 0)) or (year % 400 == 0):
        return True
    else:
        return False


# --- Check if a date if valid ---
def is_vaild_date(year: int, month: int, date: int) -> bool:
    if (date not in range(1,32)) or (month not in range(1,13)) or (year < 1):
        return False
    if month in [4,6,9,11] and date == 31:
        return False
    if month == 2 and date > 28:
        if is_leap(year) and date <= 29:
            return True
        else:
            return False
    else:
        return True


# --- Command: daysleft ---
@app_commands.command(name="daysleft", description=text("cmd.daysleft.description"))
@app_commands.describe(
    year=text("cmd.daysleft.year"),
    month=text("cmd.daysleft.month"),
    date=text("cmd.daysleft.date"),
    add=text("cmd.daysleft.add")
)
@app_commands.choices(
    add = [
        Choice(name=text("cmd.daysleft.yes"), value=1),
        Choice(name=text("cmd.daysleft.no"), value=0)
    ]
)
async def daysleft(
    interaction: discord.Interaction,
    year: app_commands.Range[int,2024,2099],
    month: app_commands.Range[int,1,12],
    date: app_commands.Range[int,1,31],
    add: Choice[int]
):
    if not is_vaild_date(year, month, date):
        await interaction.response.send_message(text("cmd.daysleft.not_valid",year,month,date))
    else:
        target = datetime.datetime(year, month, date)
        today = datetime.datetime.now()

        days_left = (target - today).days + 1
        if add.value: days_left += 1

        embed = discord.Embed(
            title=text("cmd.daysleft.left", days_left),
            description=text("cmd.daysleft.target",year,month,date),
            timestamp=datetime.datetime.now()
        )
        if add.value:
            title += text("cmd.daysleft.included")
        await interaction.response.send_message(embed=embed)