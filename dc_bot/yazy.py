import discord
from discord import app_commands
from discord.app_commands import Choice
import random


class RollDice:
    def __init__(self) -> None:
        self.times: int = 3
        self.rolls = [0]*5
        self.holds = [False]*5
        # 1, 2, 3, 4, 5, 6, 333, 4444, 33322, 12345, 55555 (Total=11)
        self.score = [0]*11
        self.preview = [0]*11
    def roll(self) -> None:
        if self.times >= 1:
            # Roll dice
            self.rolls = [random.randint(1,6) if not self.holds[i] else self.rolls[i] for i in range(5)]
            self.times -= 1
            # Preview scores
            appear_times = [self.rolls.count(i+1) for i in range(6)]  # ex: [6,6,1,1,3] -> [2,0,1,0,0,2] 
            self.preview[0] = sum([i for i in self.rolls if i == 1])                # 1
            self.preview[1] = sum([i for i in self.rolls if i == 2])                # 2
            self.preview[2] = sum([i for i in self.rolls if i == 3])                # 3
            self.preview[3] = sum([i for i in self.rolls if i == 4])                # 4
            self.preview[4] = sum([i for i in self.rolls if i == 5])                # 5
            self.preview[5] = sum([i for i in self.rolls if i == 6])                # 6
            self.preview[6] = sum(self.rolls) if 3 in appear_times else 0           # 333
            self.preview[7] = sum(self.rolls) if 4 in appear_times else 0           # 4444
            self.preview[8] = 25 if 3 in appear_times and 2 in appear_times else 0  # 33322
            self.preview[9] = 40 if appear_times.count(1) == 5 else 0               # 12345
            self.preview[10] = 50 if 5 in appear_times else 0                       # 55555
            for i in range(11):
                if self.score[i]:
                    self.preview[i] = '-'
    def confirm(self, index: int) -> bool:
        if self.preview[index] != '-':
            self.score[index] = self.preview[index]
            self.preview = [0]*11
            self.times = 3
            self.rolls = [0]*5
            self.holds = [False]*5
            return True
        else: return False

participants = []
playerdata = []

def check_player(interaction: discord.Interaction):
    global participants, playerdata
    name = str(interaction.user)
    if name not in participants:
        participants.append(name)
        playerdata.append(name)
        playerdata[len(playerdata)-1] = RollDice()
    return playerdata[participants.index(name)]

@app_commands.command(name="yazyreset", description="[Yazy] 清除所有人的Yazy遊玩紀錄")
async def yazyreset(interaction: discord.Interaction):
    global participants, playerdata
    participants = []
    playerdata = []
    await interaction.response.send_message("[Yazy] 已清除所有數據並準備好要開始")

@app_commands.command(name="yazystart", description="[Yazy] 開始一場新的Yazy遊戲，只會清除自己的紀錄")
async def yazystart(interaction: discord.Interaction):
    global participants, playerdata
    name = str(interaction.user)
    if name in participants:
        i = participants.index(name)
        participants.pop(i)
        playerdata.pop(i)
        await interaction.response.send_message(f"[Yazy] 已清除{interaction.user}的紀錄")
    else:
        await interaction.response.send_message(f"[Yazy] 找不到{interaction.user}的紀錄")


@app_commands.command(name="yazyroll", description="[Yazy] 擲骰子")
async def yazyroll(interaction: discord.Interaction):
    player = check_player(interaction)  
    if player.times != 0:
        player.roll()
        left = player.times
        result = player.rolls
        prev = player.preview

        result = [f"{result[i]}[固定]" if player.holds[i] else result[i] for i in range(len(result))]

        embed = discord.Embed(
            title=f"{result[0]}, {result[1]}, {result[2]}, {result[3]}, {result[4]}",
            description=f"{str(interaction.user)}本回你還剩{left}次機會\n使用 [/yazyhold] 來固定骰子\n使用 [/yazychoose] 來選擇分數並進入下回合\n使用 [/yazyroll] 再骰一次",
            color=discord.Color.yellow()
        )
        embed.add_field(name="[1] 1", value=prev[0], inline=True)
        embed.add_field(name="[2] 2", value=prev[1], inline=True)
        embed.add_field(name="[3] 3", value=prev[2], inline=True)
        embed.add_field(name="[4] 4", value=prev[3], inline=True)
        embed.add_field(name="[5] 5", value=prev[4], inline=True)
        embed.add_field(name="[6] 6", value=prev[5], inline=True)
        embed.add_field(name="[7] 333", value=prev[6], inline=True)
        embed.add_field(name="[8] 4444", value=prev[7], inline=True)
        embed.add_field(name="[9] 33322", value=prev[8], inline=True)
        embed.add_field(name="[10] 12345", value=prev[9], inline=True)
        embed.add_field(name="[11] 55555", value=prev[10], inline=True)
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("本回合剩餘次數：0，已無法再骰，請使用 [/yazychoose] 來選擇分數並進入下回合")

@app_commands.command(name="yazychoose", description="[Yazy] 選擇分數並進入下個回合")
@app_commands.describe(index="編號 (使用 [/yazyroll] 後的項目前綴編號)")
async def yazychoose(interaction: discord.Interaction, index: int):
    player = check_player(interaction)
    index -= 1
    if player.preview[index] == '-':
        await interaction.response.send_message("無法選擇已骰過的分數")
        return
    else:
        if player.confirm(index=index):
            await interaction.response.send_message("選擇成功，使用 [/yazyscore] 來查看所有分數")
            return
        else:
            await interaction.response.send_message("選擇失敗，請再試一次")


@app_commands.command(name="yazyhold", description="[Yazy] 固定骰子")
@app_commands.describe(holds="選擇骰子，輸入整數1~5 (1最左5最右)，輸入多顆時以空格分開")
async def yazyhold(
    interaction: discord.Interaction,
    holds: str,
):
    holdlist = holds.split(" ")
    try:
        holdlist = [int(i)-1 for i in holdlist if int(i)-1 in (0,1,2,3,4)]
        if len(holdlist) == 0:
            await interaction.response.send_message("無效的輸入")
            return
    except Exception as e:
        await interaction.response.send_message(f"無效的輸入\n{e}")
        return

    player = check_player(interaction)
    for i in holdlist:
        player.holds[int(i)] = False if player.holds[int(i)] else True
    
    embed = discord.Embed(
        title = f"{player.rolls[0]}{'[固定]' if player.holds[0] else ''}, " +
                f"{player.rolls[1]}{'[固定]' if player.holds[1] else ''}, " +
                f"{player.rolls[2]}{'[固定]' if player.holds[2] else ''}, " +
                f"{player.rolls[3]}{'[固定]' if player.holds[3] else ''}, " +
                f"{player.rolls[4]}{'[固定]' if player.holds[4] else ''}",
        description = str(interaction.user),
        color = discord.Color.yellow()
    )
    
    await interaction.response.send_message(embed=embed)


@app_commands.command(name="yazyscore", description="[Yazy] 顯示目前得分")
async def yazyscore(interaction: discord.Interaction):
    player = check_player(interaction)
    score = player.score

    embed = discord.Embed(
        title="目前得分",
        description=f"{str(interaction.user)}目前得分：{sum([i for i in score if i != '-'])}\n沒顯示的皆為0分",
        color=discord.Color.yellow()
    )
    if score[0]: embed.add_field(name="1", value=score[0], inline=True)
    if score[1]: embed.add_field(name="2", value=score[1], inline=True)
    if score[2]: embed.add_field(name="3", value=score[2], inline=True)
    if score[3]: embed.add_field(name="4", value=score[3], inline=True)
    if score[4]: embed.add_field(name="5", value=score[4], inline=True)
    if score[5]: embed.add_field(name="6", value=score[5], inline=True)
    if score[6]: embed.add_field(name="333", value=score[6], inline=True)
    if score[7]: embed.add_field(name="4444", value=score[7], inline=True)
    if score[8]: embed.add_field(name="33322", value=score[8], inline=True)
    if score[9]: embed.add_field(name="12345", value=score[9], inline=True)
    if score[10]: embed.add_field(name="55555", value=score[10], inline=True)
    await interaction.response.send_message(embed=embed)


