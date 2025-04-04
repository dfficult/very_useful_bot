# === eat.py ===
import discord
from discord import app_commands
from discord.app_commands import Range
import random
from typing import Optional
from lang import *

# --- Prefixs ---
prefixs = text("eat.prefix")
ends = text("eat.ends")


# --- Command: eat ---
@app_commands.command(name="eat", description=text("cmd.eat.description"))
@app_commands.describe(amount=text("cmd.amount"))
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
@app_commands.command(name="addfood", description=text("cmd.addfood.description"))
@app_commands.describe(food=text("cmd.addfood.food"))
async def addfood(interaction: discord.Interaction, food: str):
    with open("assets/foodlist.txt","r",encoding="UTF-8") as f:
        contents = f.readlines()
        foodlist = [i.strip() for i in contents]
    if food not in foodlist:
        with open("assets/foodlist.txt","w",encoding="UTF-8") as f:
            foodlist.append(food)
            for i in foodlist: f.write(f"{i}\n")
        await interaction.response.send_message(text("cmd.addfood.success",food))
    else:
        await interaction.response.send_message(text("cmd.addfood.exist"),food)