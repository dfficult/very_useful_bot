import discord
from discord import app_commands
from discord.ui import Button, View



class Calculator(View):
    def __init__(self):
        super().__init__()
        self.screen: str = "0"

        buttons = [
            ["(", ")", "⌫", "AC"],# Row 1
            ["7", "8", "9", "÷"],  # Row 2
            ["4", "5", "6", "×"],  # Row 3
            ["1", "2", "3", "-"],  # Row 4
            ["0", ".", "=", "+"]   # Row 5
        ]
        styles = [
            [discord.ButtonStyle.primary, discord.ButtonStyle.primary, discord.ButtonStyle.primary, discord.ButtonStyle.danger],
            [discord.ButtonStyle.secondary, discord.ButtonStyle.secondary, discord.ButtonStyle.secondary, discord.ButtonStyle.primary],
            [discord.ButtonStyle.secondary, discord.ButtonStyle.secondary, discord.ButtonStyle.secondary, discord.ButtonStyle.primary],
            [discord.ButtonStyle.secondary, discord.ButtonStyle.secondary, discord.ButtonStyle.secondary, discord.ButtonStyle.primary],
            [discord.ButtonStyle.secondary, discord.ButtonStyle.secondary, discord.ButtonStyle.success, discord.ButtonStyle.primary],
        ]
        for i in range(len(buttons)):
            for j in range(len(buttons[i])):
                button = Button(label=buttons[i][j], style=styles[i][j], row=i,custom_id=buttons[i][j])
                button.callback = self.button_callback
                self.add_item(button)
        
    async def button_callback(self, interaction: discord.Interaction):
        button = interaction.data["custom_id"]

        if button == "AC":
            self.screen = "0"
        elif button == "⌫":
            self.screen = self.screen[0:len(self.screen)-1]
            if self.screen == '': self.screen = '0'
        elif button == "=":
            result = self.screen.replace("×", "*").replace("÷", "/").replace("%", "*0.01")
            try:
                result = eval(result)
            except ZeroDivisionError:
                embed = discord.Embed(
                    title=f"{interaction.user.name}，您已被永久禁止使用計算機",
                    description="違反服務條款：嘗試將數字除以0",
                    color=discord.Color.red()
                )
                global blacklist
                blacklist.append(interaction.user.name)
                with open("calculator_blacklist.txt", "w") as file:
                    for item in blacklist:
                        file.write(f"{item}\n")
                await interaction.message.delete()
                await interaction.response.send_message(embed=embed)
                return
            except Exception as e:
                result = e
            self.screen = '0'
            await self.update_calculator(interaction, result)
            return

        else:
            if button == '.' and (self.screen[len(self.screen)-1] not in ['1','2','3','4','5','6','7','8','9']):
                self.screen += "0."
            elif self.screen == '0' and (button not in ['+', '-', '×', '÷', '%']):
                self.screen = button
            else:
                self.screen += button
        await self.update_calculator(interaction)



    async def update_calculator(self, interaction: discord.Interaction, *args):
        embed = discord.Embed(
            title="",
            description=f"# ```{self.screen}```",
            color=discord.Color.yellow()
        )
        if args:
            embed.description = f"# ```{args[0]}```"
        await interaction.response.edit_message(embed=embed, view=self)

with open("calculator_blacklist.txt", "r") as file:
    blacklist = [line.strip() for line in file]


@app_commands.command(name="calculator", description="[計算機] 開啟計算機")
@app_commands.describe()
async def calculator(interaction: discord.Interaction):
    global blacklist
    if interaction.user.name in blacklist:
        await interaction.response.send_message("您已被永久禁止使用計算機")
        return
    embed = discord.Embed(
        title="",
        description=f"# ```0```",
        color=discord.Color.yellow()
    )
    await interaction.response.send_message(embed=embed, view=Calculator())