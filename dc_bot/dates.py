# === dates.py ===
import discord
from discord import app_commands
from discord.app_commands import Choice
import datetime


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
@app_commands.command(name="daysleft", description="[日期] 新增日期倒數")
@app_commands.describe(
    year="輸入年分",
    month="輸入月份",
    date="輸入日期",
    add="包含第一天"
)
@app_commands.choices(
    add = [
        Choice(name="是 (加一天)", value=1),
        Choice(name="否 (不加一天)", value=0)
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
        await interaction.response.send_message(f"{year}/{month}/{date} 不是一個有效的日期")
    else:
        target = datetime.datetime(year, month, date)
        today = datetime.datetime.now()

        days_left = (target - today).days + 1
        if add.value: days_left += 1

        embed = discord.Embed(
            title=f"剩餘{days_left}天{' (包含第一天)' if add.value else ''}",
            description=f"目標日期：{year}/{month}/{date}",
            timestamp=datetime.datetime.now()
        )
        await interaction.response.send_message(embed=embed)