import discord
from discord import app_commands
import random

# Load all foods
with open("foodlist.txt","r",encoding="UTF-8") as f:
    contents = f.readlines()
foodlist = [i.strip() for i in contents]

# Prefixs
prefixs = ["就吃","我覺得","必須是","吃","為什麼不來點","今晚，我想來點","我推薦","幫我點","好久沒吃","跟你說我要吃"]
ends = ["吧","是個不錯的選擇","的吧","就對了","呢?","\n(應該) 都點的到","","，謝謝 <3","了","，到底要問幾次"]


@app_commands.command(name="eat", description=f"[隨機] 從食物清單中挑選出一種食物")
async def eat(interaction: discord.Interaction):
    i = random.randint(0, len(foodlist)-1)
    j = random.randint(0, len(prefixs)-1)
    await interaction.response.send_message(f"{prefixs[j]}{foodlist[i]}{ends[j]}")

@app_commands.command(name="addfood", description=f"[隨機] 新增食物到食物清單")
@app_commands.describe(food="食物")
async def addfood(interaction: discord.Interaction, food: str):
    if food not in foodlist:
        with open("foodlist.txt","w",encoding="UTF-8") as f:
            foodlist.append(food)
            for i in foodlist: f.write(f"{i}\n")
        await interaction.response.send_message(f"成功新增{food}")
    else:
        await interaction.response.send_message(f"{food}已存在")

@app_commands.command(name="gowhere", description="[隨機] 要往哪裡走呢?")
async def gowhere(interaction: discord.Interaction):
    directions = ["前", "後"]
    turns = ["左","右"]
    match random.randint(1,3):
        case 1:
            await interaction.response.send_message(
                f"往{directions[random.randint(0,len(directions)-1)]}走{random.randint(1,6)*5}公尺"
            )
        case 2:
            await interaction.response.send_message(
                f"向{turns[random.randint(0,len(turns)-1)]}轉"
            )
        case 3:
            await interaction.response.send_message(
                f"目的地在你的{turns[random.randint(0,len(turns)-1)]}手邊"
            )