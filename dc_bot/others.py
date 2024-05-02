import discord
from discord import app_commands

@app_commands.command(name="which_day_next_sun", description="下個禮拜天是星期幾?")
async def which_day_next_sun(interaction: discord.Interaction):
    await interaction.response.send_message("下個禮拜天是星期天。")
