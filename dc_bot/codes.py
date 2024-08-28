# === codes.py ===
# not completed yet
import discord
from discord import app_commands
import json, os, subprocess


# --- SubmitWindow ---
class SubmitWindow(discord.ui.Modal, title="提交程式碼"):
    codes = discord.ui.TextInput(
        style=discord.TextStyle.paragraph,
        label="C++",
        required=True,
        placeholder="請輸入C++程式碼"
    )

    async def on_submit(self, interaction: discord.Interaction):
        # load the data about this test
        global id_global
        with open(f"code_test/{id_global}.json", "r") as file:
           question = json.load(file)
        
        # prepare for discord embed
        embed = discord.Embed(
            title=f"#{id_global}",
            description="description",
            color=discord.Color.gold()
        )
        
        # load the cpp file
        codes = self.codes.value
        with open("test.cpp", "w") as file:
            file.write(codes)

        # interaction must be sent within 3 seconds, so we need this
        await interaction.response.defer(thinking=True)

        # run code for every test data
        amount = len(question["tests"])
        passed = 0             # passed count
        errors = ["0"]*amount    # wrong output
        for i in range(amount):
            # load input data
            with open("input.txt", "w") as file:
                file.write(question["tests"][i]["input"])
            # let's run it
            runcode_path = "./runcode.sh"
            result = subprocess.run(["bash", runcode_path], capture_output=True, text=True)
            # check the result
            if result.stderr:
                # An error occurred
                embed.description = "Error"
                embed.add_field(name=f"Test {i+1}: Error", value=result.stderr)
                await interaction.followup.send(embed=embed)
                return
            else:
                if result.stdout == question["tests"][i]["output"]:
                    # Correct
                    passed += 1
                else:
                    # Wrong
                    errors[i] = result.stdout
        
        # send the results to the user
        embed.description = f"Passed: {passed}/{amount}"
        for i in range(amount):
            if errors[i] == "0":
                embed.description += f"\nTest{i+1}: Passed"
            else:
                embed.description += f"\nTest{i+1}: Failed"
                embed.add_field(name=f"Test{i+1} input", value=question["tests"][i]["input"])
                embed.add_field(name=f"Test{i+1} expected output", value=question["tests"][i]["output"])
                embed.add_field(name=f"Test{i+1} your output", value=errors[i])
        await interaction.followup.send(embed=embed)

    async def on_error(self, interaction: discord.Interaction, error):
        print(error)  # prints error


# --- Command: code ---
@app_commands.command(name="code", description="[程式] 選擇程式題目")
@app_commands.describe(id="題目編號 (xxxx)")
async def code(interaction: discord.Interaction, id: str):
#    get_compiler_ver()
   file_path = f"code_test/{id}.json"
   if os.path.exists(file_path):
        with open(file_path, "r") as file:
           question = json.load(file)
        
        embed = discord.Embed(
            title=question["name"],
            description=f"{question['question']}\n\n  ",
            color=discord.Color.gold()
        )
        
        embed.add_field(name="輸入格式", value=question["input_format"], inline=True)
        embed.add_field(name="輸出格式", value=f"{question['output_format']}\n  ", inline=True)   
        
        examples = question["examples"]
        for i in range(len(examples)):
            embed.add_field(name=f"範例輸入{i+1}", value=examples[i]["input"], inline=True)
            embed.add_field(name=f"範例輸出{i+1}", value=f"{examples[i]['output']}\n  ", inline=True)

        embed.add_field(name="提交程式碼", value=f"使用 `/submit_code id:{id}` 來開啟輸入視窗\n語言：C++\n記憶體限制：256MB")

        match question["difficulty"]:
            case 0: difficulty = "簡單"
            case 1: difficulty = "普通"
            case 2: difficulty = "中等"
            case 3: difficulty = "困難"
            case _: difficulty = "未知"
        embed.set_footer(text=f"難易度：{difficulty} | 來源：{question['from']}")
        embed.set_author(name=f"#{id}")

        await interaction.response.send_message(embed=embed)
   else:
        await interaction.response.send_message(f"id {id} does not exist", ephemeral=True)


# --- Command: submit_code ---
@app_commands.command(name="submit_code", description="[程式] 提交程式碼")
@app_commands.describe(id="題目編號 (xxxx)")
async def submit_code(interaction: discord.Interaction, id: str):
    file_path = f"code_test/{id}.json"
    if os.path.exists(file_path):
       global id_global
       id_global = id
       await interaction.response.send_modal(SubmitWindow())
    else:
        await interaction.response.send_message(f"id {id} does not exist", ephemeral=True)
    