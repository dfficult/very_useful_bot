import discord
from discord import app_commands
import json
import datetime


@app_commands.command(name="mborrow", description="[記帳] 紀錄誰欠你錢")
@app_commands.describe(user="輸入欠你錢的人 (@...)", amount="輸入金額 (正整數，不用加上$或單位)")
async def mborrow(interaction: discord.Interaction, user: discord.User, amount: int):
    creditor: str = str(interaction.user)

    this = {
        "year": datetime.datetime.now().year,
        "month": datetime.datetime.now().month,
        "date": datetime.datetime.now().day,
        "hour": datetime.datetime.now().hour,
        "minute": datetime.datetime.now().minute,
        "debtor": str(user),
        "amount": amount
    }

    # 5:6 -> 5:06
    this["minute"] = f"0{this['minute']}" if len(str(this["minute"])) == 1 else this["minute"]

    with open("money.json", "r") as f:
        data = json.load(f)
    
    if creditor in data:
        data[creditor].append(this)
    else:
        data[creditor] = [this]
    
    with open("money.json", "w") as f:
        f.write(json.dumps(data, indent=4))
    
    embed = discord.Embed(
        title="紀錄儲存成功!",
        description=f"{str(user)}欠你{amount}",
        timestamp=datetime.datetime.now(),
        color=discord.Color.green()
    )

    await interaction.response.send_message(embed=embed)
        

@app_commands.command(name="mhistory", description="[記帳] 查看誰欠你錢")
async def mhistory(interaction: discord.Interaction):
    creditor: str = str(interaction.user)
    
    embed = discord.Embed(
        title=f"{creditor}借錢出去的紀錄",
        color=discord.Color.green()
    )
    
    with open("money.json", "r") as f:
        data = json.load(f)
    
    j = 1
    m = 0
    if creditor in data:
        for i in data[creditor]:
            embed.add_field(
                name=f"[{j}] {i['debtor']}欠你{i['amount']}",
                value=f"{i['year']}/{i['month']}/{i['date']} {i['hour']}:{i['minute']}"
            )
            j += 1
            m += i["amount"]
    
    embed.description = f"共{j-1}筆紀錄，金額總和{m}元"

    await interaction.response.send_message(embed=embed)
        

@app_commands.command(name="mdelete", description="[記帳] 刪除紀錄")
@app_commands.describe(option="編號 (使用 [/mhistory] 來查看紀錄編號)")
async def mdelete(interaction: discord.Interaction, option: int):
    option -= 1
    
    creditor: str = str(interaction.user)
    
    with open("money.json", "r") as f:
        data = json.load(f)
    

    if creditor in data:
        try:
            del data[creditor][option]
            with open("money.json", "w") as f:
                f.write(json.dumps(data, indent=4))
            await interaction.response.send_message("紀錄刪除成功")
        except Exception as e:
            await interaction.response.send_message(f"編號 {option+1} 無法刪除，請確認編號後再試一次\n{e}")

    else:
        await interaction.response.send_message("很棒，沒有任何人欠你錢！")