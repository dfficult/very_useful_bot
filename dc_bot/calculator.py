import discord
from discord import app_commands
from discord.ui import Button, View
import settings
from lang import *

class Calculator(View):
    def __init__(self):
        super().__init__()
        self.screen: str = "0"

        buttons = [
            ["(", ")", text("calculator.backspace"), text("calculator.clear_all")],# Row 1
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

        if button == text("calculator.clear_all"):
            self.screen = "0"
        elif button == text("calculator.backspace"):
            self.screen = self.screen[0:len(self.screen)-1]
            if self.screen == '': self.screen = '0'
        elif button == "=":
            result = self.screen.replace("×", "*").replace("÷", "/").replace("%", "*0.01")
            try:
                result = eval(result)
            except ZeroDivisionError:
                embed = discord.Embed(
                    title=text("calculator.banned", interaction.user.name),
                    description=text("calculator.banned_reason"),
                    color=settings.Colors.fail
                )
                global blacklist
                blacklist.append(interaction.user.name)
                with open("assets/calculator_blacklist.txt", "w") as file:
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
            color=settings.Colors.math
        )
        if args:
            embed.description = f"# ```{args[0]}```"
        await interaction.response.edit_message(embed=embed, view=self)

with open("assets/calculator_blacklist.txt", "r") as file:
    blacklist = [line.strip() for line in file]


@app_commands.command(name="calculator", description=text("cmd.calculator.description"))
@app_commands.describe()
async def calculator(interaction: discord.Interaction):
    global blacklist
    if interaction.user.name in blacklist:
        await interaction.response.send_message(text("cmd.calculator.banned"))
        return
    embed = discord.Embed(
        title="",
        description=f"# ```0```",
        color=settings.Colors.math
    )
    await interaction.response.send_message(embed=embed, view=Calculator())


@app_commands.context_menu(name=text("menu.evaluate"))
async def calculate(interaction: discord.Interaction, message: discord.Message):
    to_calculate = message.content
    to_calculate = to_calculate.replace(" ", "")
    to_calculate = to_calculate.rstrip("=")
    try:
        result = eval(to_calculate)
        await interaction.response.send_message(f"{to_calculate} = **{result}**")
    except Exception as e:
        await interaction.response.send_message(text("menu.evaluate.fail", e))