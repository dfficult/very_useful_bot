# === notice.py ===
import discord
from discord import app_commands
from discord.app_commands import Choice, Range
import datetime, json



# --- Settings ---
NOTICE_COLOR = discord.Color.dark_magenta()



# --- All the notice events are stored here ---
events = []
def sync_json():
    with open("assets/notice.json", "w") as f:
        f.write(json.dumps(events, indent=4))


# --- Prefix zero ---
def pre_zero(tofix: int) -> str:
    if tofix < 10:
        return "0" + str(tofix)
    else:
        return str (tofix)


# --- Command: notice ---
@app_commands.command(name="notice_after", description="[提醒] 在一段時間後提醒")
@app_commands.describe(event="輸入事件名稱", time="輸入時間", unit="時間單位")
@app_commands.choices(
    unit=[
        Choice(name="分鐘", value="m"),
        Choice(name="小時", value="h"),
        Choice(name="天", value="d")
    ]
)
async def notice_after(interaction: discord.Interaction, event: str, time: Range[int, 1, 60], unit: Choice[str]):
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
        title="已設置提醒",
        description=f"## {event}",
        timestamp=datetime.datetime.now(),
        color=NOTICE_COLOR
    )
    embed.add_field(name="觸發提醒", value=after)
    embed.add_field(name="提醒時間", value=f"{target.year}/{target.month}/{target.day} {pre_zero(target.hour)}:{pre_zero(target.minute)}")
    await interaction.response.send_message(embed=embed)


# --- Command: notice ---
@app_commands.command(name="notice_at", description="[提醒] 在特定時間提醒")
@app_commands.describe(event="輸入事件名稱", year="年", month="月", day="日")
@app_commands.choices(
    year=[Choice(name=i, value=i) for i in range(2025, 2030)],
    month=[Choice(name=i, value=i) for i in range(1, 13)],
)
async def notice_at(interaction: discord.Interaction, event: str, year: Choice[int], month: Choice[int], day: Range[int, 1, 31], hour: Range[int, 1, 60], minute: Range[int, 1, 60]):
    # check no same name
    for i in events:
        if i["event"] == event:
            await interaction.response.send_message("該提醒事件已存在，請換別的名稱")
            return

    # save target
    tar = {
        "year": year.value,
        "month": month.value,
        "day": day,
        "hour": hour,
        "minute": minute,
        "event": event,
        "channel": interaction.channel_id,
        "user": interaction.user.id
    }
    events.append(tar)
    sync_json()

    embed = discord.Embed(
        title="提醒已設置",
        description=f"## {event}",
        timestamp=datetime.datetime.now(),
        color=NOTICE_COLOR
    )
    embed.add_field(name="提醒時間", value=f"{year.value}/{month.value}/{day} {pre_zero(hour)}:{pre_zero(minute)}")
    await interaction.response.send_message(embed=embed)


# --- Command: delnotice ---
class DropDown(discord.ui.Select):
    def __init__(self, user_id):
        selects = [
            discord.SelectOption(label=i["event"], description=f"{i['year']}/{i['month']}/{i['day']} {pre_zero(i['hour'])}:{pre_zero(i['minute'])}", value=i['event']) for i in events if i["user"] == user_id
        ]
        selects.append(discord.SelectOption(label="取消刪除", description="選取此項關閉刪除選單", value="CANCEL"))
        super().__init__(placeholder="選擇要刪除的提醒事項", min_values=1, max_values=1, options=selects)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "CANCEL":
            await interaction.response.defer()
            await interaction.delete_original_response()
            return
        for i in events:
            if i["event"] == self.values[0]:
                events.remove(i)
                sync_json()
                await interaction.response.defer()
                await interaction.edit_original_response(content=f"已刪除提醒事項：{self.values[0]}", view=None)
                return
        await interaction.response.defer()
        await interaction.edit_original_response(content="發生了未知的錯誤，請稍後再試", view=None)



class DropDownView(discord.ui.View):
    def __init__(self, user_id):
        super().__init__()
        self.add_item(DropDown(user_id=user_id))



@app_commands.command(name="notice_delete", description="[提醒] 選擇提醒事項並刪除")
@app_commands.describe()
async def notice_delete(interaction: discord.Interaction):
    await interaction.response.send_message("在下方選單中選擇要刪除的提醒事項", view=DropDownView(interaction.user.id), delete_after=15, ephemeral=True)

# --- load json upon starting veryusefulbot ---
with open("assets/notice.json", "r") as f:
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
                color=NOTICE_COLOR,
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