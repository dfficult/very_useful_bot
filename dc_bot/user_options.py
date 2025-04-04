import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ui import Button, View
import os, json
import settings


class Options:
    def __init__(self, type: any, default: any):
        self.type = type
        self.default = default

def is_color(value: str) -> bool:
    if value[0] != "#":
        return False
    for i in value:
        if i not in "#0123456789abcdefABCDEF":
            return False
    return True



defaults = {
    "WordleBackgroundColor": Options("color", "#2E2E34"),
    "WordleBlockSize": Options("int", 50),
    "WordleBlockMargin": Options("int", 5),
    "WordleFontColor": Options("color", "#FFFFFF"),
    "WordleGrayColor": Options("color", "#3A3A3C"),
    "WordleGreenColor": Options("color", "#538D4E"),
    "WordleImageMargin": Options("int", 0),
    "WordleYellowColor": Options("color", "#B59F3B")
}




def get_user_options(user_id: int, option_id: str) -> any:
    path = f"assets/user_options/{user_id}.json"
    if os.path.exists(path):
        with open(path, "r") as file:
            options = json.load(file)
        try:
            # return the key
            return options[option_id]
        except KeyError:
            # key not found
            return defaults[option_id].default
    else:
        # file does not exist
        return defaults[option_id].default



@app_commands.command(name="option", description="[選項] 變更個人指令選項")
@app_commands.describe(key="key", value="value")
@app_commands.choices(key = [Choice(name=i, value=i) for i in defaults.keys()])
async def option(interaction: discord.Interaction, key: Choice[str], value: str):
    # Check if value is valid
    if key.value not in defaults.keys():
        await interaction.response.send_message(f"Key `{key.value}` 不存在")
        # raise ValueError(f"Key {key.value} does not exist.")
        return
    match defaults[key.value].type:
        case "color":
            if not is_color(value):
                await interaction.response.send_message(f"`{value}` 的類別不是 `color`")
                # raise ValueError(f"'{value}' is not a color, expected type is color.")
                return
        case "int":
            try:
                value = int(value)
            except Exception as e:
                await interaction.response.send_message(f"`{value}` 的類別不是 `int`")
                # raise ValueError(f"'{value}' is not an int, expected type is int. Error: {e}")
                return
        case "str":
            # What could possibly go wrong?
            pass
    
    # Open file
    path = f"assets/user_options/{interaction.user.id}.json"
    if os.path.exists(path):
        with open(path, "r") as f:
            options = json.load(f)
    else:
        options = {i: j.default for i, j in defaults.items()}

    # Change option
    options[key.value] = value

    # Write back file
    with open(path, "w") as f:
        f.write(json.dumps(options, indent=4))

    # Output
    embed = discord.Embed(
        title="已變更選項",
        description=f"**`{key.value}`** 已設為 **`{value}`** (預設: `{defaults[key.value].default}`)",
        color=settings.Colors.success
    )
    await interaction.response.send_message(embed=embed)
