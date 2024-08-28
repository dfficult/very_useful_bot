# === notice.py ===
import discord
from discord import app_commands
from discord.app_commands import Choice, Range
import datetime, json


# --- All the notice events are stored here ---
events = []
def sync_json():
    with open("notice.json", "w") as f:
        f.write(json.dumps(events, indent=4))


# --- Prefix zero ---
def pre_zero(tofix: int) -> str:
    if tofix < 10:
        return "0" + str(tofix)
    else:
        return str (tofix)


# --- Command: notice ---
@app_commands.command(name="notice", description="[提醒] 新增提醒事項")
@app_commands.describe(event="輸入事件名稱", time="輸入時間", unit="時間單位")
@app_commands.choices(
    unit=[
        Choice(name="分鐘", value="m"),
        Choice(name="小時", value="h"),
        Choice(name="天", value="d")
    ]
)
async def notice(interaction: discord.Interaction, event: str, time: Range[int, 1, 60], unit: Choice[str]):
    # check no same name
    for i in events:
        if i["event"] == event:
            await interaction.response.send_message("該提醒事件已存在，請換別的名稱")
            return
    # calculate target
    now = datetime.datetime.now()
    match unit.value:
        case "m": target = now + datetime.timedelta(minutes=time)
        case "h": target = now + datetime.timedelta(hours=time)
        case "d": target = now + datetime.timedelta(days=time)

    # save target
    tar = {
        "year": target.year,
        "month": target.month,
        "day": target.day,
        "hour": target.hour,
        "minute": target.minute,
        "event": event,
        "channel": interaction.channel_id,
        "user": interaction.user.id
    }
    events.append(tar)
    sync_json()

    match unit.value:
        case "m": after = f"{time}分鐘後"
        case "h": after = f"{time}小時後"
        case "d": after = f"{time}天後"
    embed = discord.Embed(
        title="提醒已設置",
        description=f"## {event}",
        timestamp=datetime.datetime.now(),
        color=discord.Color.red()
    )
    embed.add_field(name="觸發提醒", value=after)
    embed.add_field(name="提醒時間", value=f"{target.month}/{target.day} {pre_zero(target.hour)}:{pre_zero(target.minute)}")
    await interaction.response.send_message(embed=embed)


# --- Command: delnotice ---
@app_commands.command(name="delnotice", description="[提醒] 刪除提醒事項")
@app_commands.describe()
async def delnotice(interaction: discord.Interaction, event: str):
    for i in events:
        if i["event"] == event:
            events.remove(i)
            sync_json()
            await interaction.response.send_message(f"已刪除 {event}")
            return
    await interaction.response.send_message(f"未找到 {event}")


# --- load json upon starting veryusefulbot ---
with open("notice.json", "r") as f:
    events = json.load(f)


# --- Put this in the loop in main.py ---
def check_notice():
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute
    if len(events) == 0: return None
    success = False
    returnlist = []
    for i in events:
        if (i["year"] == year and
            i["month"] == month and
            i["day"] == day and
            i["hour"] == hour and
            i["minute"] == minute
        ):
            success = True
            embed = discord.Embed(
                title="提醒",
                description=f'## {i["event"]}',
                color=discord.Color.red(),
                timestamp=datetime.datetime.now()
            )
            channel = i["channel"]
            user = i["user"]
            events.remove(i)
            sync_json()
            returnlist.append([user, channel, embed])
    if success:
        return returnlist
    else:
        return None