import discord
from discord import app_commands

class DropDown(discord.ui.Select):
    def __init__(self):
        selects = [
            discord.SelectOption(label="Option A", description="Never gonna give you up", value="a"),
            discord.SelectOption(label="Option B", description="Never gonna let you down", value="b"),
            discord.SelectOption(label="Option C", description="Never gonna run around and desert you", value="c")
        ]
        super().__init__(placeholder="選擇要固定的骰子", min_values=1, max_values=1, options=selects)

        async def callback(self, interaction: discord.Interaction):
            await interaction.response.send_message(f"u chose {self.values[0]}")

class DropDownView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(DropDown())

@app_commands.command(name="test0", description="測試指令0")
async def test0(interaction: discord.Interaction):
    await interaction.response.send_message(view=DropDownView())