# === flashcard.py ===
import discord, json
from discord import app_commands
from discord.ui import Button, View
from discord.app_commands import Choice
from typing import Optional


class FlashCardBox(View):
    def __init__(self, current_index, word_list, word_list_name):
        super().__init__()
        self.current_index = current_index
        self.word_list = word_list
        self.word_list_name = word_list_name
        self.showing_word = True
        
        # Buttons
        self.previous_button = Button(label="上一個", style=discord.ButtonStyle.secondary)
        self.toggle_button = Button(label="中/英", style=discord.ButtonStyle.success)
        self.next_button = Button(label="下一個", style=discord.ButtonStyle.primary)

        # Buttons Callback
        self.previous_button.callback = self.previous_flashcard
        self.toggle_button.callback = self.toggle_meaning
        self.next_button.callback = self.next_flashcard

        # Buttons Display Order
        self.add_item(self.previous_button)
        self.add_item(self.toggle_button)
        self.add_item(self.next_button)


    async def update_message(self, interaction: discord.Interaction):
        current = self.word_list[self.current_index]

        embed = discord.Embed(
            title = "",
            description="# " + current['word'] if self.showing_word else "# " + current['meaning'],
            color=discord.Color.blue() if self.showing_word else discord.Color.green()
        )
        if not self.showing_word:
            embed.description += f"\n {current['word']}"
        embed.set_footer(text=f"{self.word_list_name}  #{self.current_index + 1}/{len(self.word_list)}")

        await interaction.response.edit_message(embed=embed, view=self)

    async def next_flashcard(self, interaction: discord.Interaction):
        self.current_index = (self.current_index + 1) % len(self.word_list)
        self.showing_word = True
        await self.update_message(interaction)

    async def previous_flashcard(self, interaction: discord.Interaction):
        self.current_index = (self.current_index - 1) % len(self.word_list)
        self.showing_word = True
        await self.update_message(interaction)

    async def toggle_meaning(self, interaction: discord.Interaction):
        self.showing_word = not self.showing_word
        await self.update_message(interaction)


# --- Command: flashcard ---
@app_commands.command(name="flashcard", description="[單字卡] 開啟單字卡")
@app_commands.choices(
    wordlist =[
        Choice(name="測試", value="測試用單字卡.json")
    ]
    
)
@app_commands.describe(wordlist="選擇單字清單", index="[Optional] 從第幾個單字開始")

async def flashcard(interaction: discord.Interaction, wordlist: Choice[str], index: Optional[int]):
    with open(f"flashcard/{wordlist.value}", "r") as f:
        word_list = json.load(f)
    
    if not index: index = 0
    index -= 1    # python starts at 0
    if index <= 0 or index > len(word_list): index = 0
    
    embed = discord.Embed(
        title="",
        description=f"# {word_list[index]['word']}",
        color=discord.Color.blue()
    )
    embed.set_footer(text=f"{wordlist.name}  #{index+1}/{len(word_list)}")

    view = FlashCardBox(current_index=index, word_list=word_list, word_list_name=wordlist.name)
    await interaction.response.send_message(embed=embed, view=view)

