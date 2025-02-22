# === eat.py ===
import discord
from discord import app_commands
from discord.app_commands import Range
import random
from typing import Optional

# --- Prefixs ---
prefixs = ["就吃","我覺得","必須是","吃","為什麼不來點","今晚，我想來點","我推薦","幫我點","好久沒吃","跟你說我要吃"]
ends = ["吧","是個不錯的選擇","的吧","就對了","呢?","\n(應該) 都點的到","","，謝謝 <3","了","，到底要問幾次"]


# --- Command: eat ---
@app_commands.command(name="eat", description=f"[隨機] 從食物清單中挑選出一種食物")
@app_commands.describe(amount="輸入數量")
async def eat(interaction: discord.Interaction, amount: Optional[Range[int, 1, 30]]):
    with open("assets/foodlist.txt","r",encoding="UTF-8") as f:
        contents = f.readlines()
        foodlist = [i.strip() for i in contents]
    if not amount: amount = 1
    selected = []
    if len(foodlist) < amount:
        amount = len(foodlist)
    selected = random.sample(foodlist, amount)
    output = str(selected)
    output = output[1:len(output)-1]
    output = output.replace("'", "")
    output = output.replace(" ", "")
    output = output.replace(",", "、")
    j = random.randint(0, len(prefixs)-1)
    await interaction.response.send_message(f"{prefixs[j]} **{output}** {ends[j]}")


# --- Command: addfood ---
@app_commands.command(name="addfood", description=f"[隨機] 新增食物到食物清單")
@app_commands.describe(food="食物")
async def addfood(interaction: discord.Interaction, food: str):
    with open("assets/foodlist.txt","r",encoding="UTF-8") as f:
        contents = f.readlines()
        foodlist = [i.strip() for i in contents]
    if food not in foodlist:
        with open("assets/foodlist.txt","w",encoding="UTF-8") as f:
            foodlist.append(food)
            for i in foodlist: f.write(f"{i}\n")
        await interaction.response.send_message(f"成功新增{food}")
    else:
        await interaction.response.send_message(f"{food}已存在")