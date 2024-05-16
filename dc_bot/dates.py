import discord
from discord import app_commands
import datetime

@app_commands.command(name="today", description="[日期] 顯示今天")
async def today(interaction: discord.Interaction):
    now = datetime.datetime.now()
    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    
    if ((now.year % 4 == 0) and (now.year % 100 != 0)) or (now.year % 400 == 0):
        y = 366
    else:
        y = 365
    december_31 = datetime.datetime(datetime.datetime.now().year - 1, 12, 31)
    now = datetime.datetime.now()
    days_passed = (now - december_31).days
    percentage = round(days_passed / y * 100, 2)

    embed = discord.Embed(
        title="今天是",
        description=f"{now.year}年{now.month}月{now.day}日  {weekdays[now.weekday()]}\n今年已經過了 {percentage}%"
    )
    await interaction.response.send_message(embed=embed)
