import discord
from discord import app_commands
import settings
from lang import *

@app_commands.context_menu(name=text("menu.wordcount"))
async def wordcount(interaction: discord.Interaction, message: discord.Message):
    try:
        word = str(message.content)
        embed = discord.Embed(
            title=text("menu.wordcount.title"),
            description="",
            color=settings.Colors.success
        )
        embed.add_field(name=text("menu.wordcount.words"), value=len(word.split(" ")))
        embed.add_field(name=text("menu.wordcount.chars"), value=len(word))
        embed.add_field(name=text("menu.wordcount.chars_no_space"), value=len(word.replace(" ", "")))
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        await interaction.response.send_message(text("menu.wordcount,err"),e)