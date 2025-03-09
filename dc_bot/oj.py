import discord
from discord import app_commands
from discord.app_commands import Choice
from typing import Optional
import json, os, subprocess, random
import settings


# --- difficulty id to name ---
def diffToName(difficulty: int) -> str: 
    match difficulty:
        case 0: return "簡單"
        case 1: return "普通"
        case 2: return "困難"



# --- SubmitWindow ---
class SubmitWindow(discord.ui.Modal, title="提交程式碼"):
    codes = discord.ui.TextInput(
        style=discord.TextStyle.paragraph,
        label="請輸入程式碼",
        required=True,
        placeholder="若要離開請先複製你的內容，此輸入框的內容不會儲存!"
    )

    async def on_submit(self, interaction: discord.Interaction):
        # load the data about this test
        global id_global #[difficulty, id]
        with open(f"assets/code_test/{id_global[0]}/{id_global[1]}.json", "r") as file:
           question = json.load(file)
        
        # prepare for discord embed
        embed = discord.Embed(
            title=f"{diffToName(id_global[0])} #{id_global[1]}",
            description="description",
            color=settings.Colors.oj
        )
        
        # save the code
        global lang
        codes = self.codes.value
        with open(f"assets/run_code/test.{lang}", "w") as file:
            file.write(codes)

        # interaction must be sent within 3 seconds, so we need this
        await interaction.response.defer(thinking=True)

        # compile the code
        result = subprocess.run(["bash", f"assets/run_code/compile_{lang}.sh"], capture_output=True, text=True)
        if result.stderr:
            # An error occurred
            embed.title = "Compilation Error"
            embed.description = result.stderr
            embed.color = settings.Colors.fail
            await interaction.followup.send(embed=embed)
            return

        # run code for every test data
        amount = len(question["tests"])
        passed = 0               # passed count
        errors = ["0"]*amount    # wrong output
        for i in range(amount):
            # load input data
            with open("assets/run_code/input.txt", "w") as file:
                file.write(question["tests"][i]["input"])
            # let's run it
            runcode_path = f"assets/run_code/run_{lang}.sh"
            result = subprocess.run(["bash", runcode_path], capture_output=True, text=True)
            # check the result
            if result.stderr:
                # An error occurred
                embed.description = "Error"
                embed.add_field(name=f"Test {i+1}: Error", value=result.stderr)
                await interaction.followup.send(embed=embed)
                return
            else:
                if result.stdout.split() == question["tests"][i]["output"].split():
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
@app_commands.command(name="code", description="[OJ] 顯示程式題目")
@app_commands.describe(difficulty="難易度", id="指定題目編號")
@app_commands.choices(
    difficulty = [
        Choice(name="簡單", value=0),
        Choice(name="普通", value=1),
        Choice(name="困難", value=2)
    ]
)
async def code(interaction: discord.Interaction, difficulty: Choice[int], id: int):
    file_path = f"assets/code_test/{difficulty.value}/{id}.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
           question = json.load(file)
        
        embed_main = discord.Embed(
            title=f"{question['name']}",
            description=f"{question['question']}\n\n  ",
            color=settings.Colors.oj
        )
        if "hint" in question:
            embed_main.add_field(name="提示", value=question['hint'], inline=False)
        embed_main.add_field(name="輸入格式", value=question['input_format'], inline=False)
        embed_main.add_field(name="輸出格式", value=f"{question['output_format']}\n  ", inline=False)   
        embed_main.add_field(name="提交程式碼", value=f"使用 `/submit_code difficulty:{diffToName(difficulty.value)} id:{id}` 開啟輸入視窗\n")
        embed_main.set_footer(text=f"來源：{question['from']}")
        if not os.path.exists(f"assets/code_test/{difficulty.value}/{id+1}.json"):
            embed_main.set_author(name=f"{diffToName(difficulty.value)} #{id} (此難易度最後一題)")
        else:
            embed_main.set_author(name=f"{diffToName(difficulty.value)} #{id}")

        embed_example = discord.Embed(
            title="範例",
            description="",
            color=settings.Colors.oj
        )
        examples = question["examples"]
        for i in range(len(examples)):
            embed_example.add_field(name=f"範例輸入{i+1}", value=examples[i]["input"], inline=False)
            embed_example.add_field(name=f"範例輸出{i+1}", value=f"{examples[i]['output']}\n  ", inline=False)
            if "description" in examples[i]:
                embed_example.add_field(name=f"範例{i+1}說明", value=examples[i]['description'], inline=False)

        await interaction.response.send_message(embeds=[embed_main, embed_example])
    else:
        await interaction.response.send_message(f"抱歉，難易度 {diffToName(difficulty.value)} 的 id{id} 不存在", ephemeral=True)


# --- Command: submit_code ---
@app_commands.command(name="submit_code", description="[OJ] 提交程式碼")
@app_commands.describe(difficulty= "難易度", id="此難易度下的題目編號", language="程式語言(C/C++)")
@app_commands.choices(
    language=[
        Choice(name="C++",value="cpp"),
        Choice(name="C",value="c")
    ],
    difficulty=[
        Choice(name="簡單", value=0),
        Choice(name="普通", value=1),
        Choice(name="困難", value=2)
    ]
)
async def submit_code(interaction: discord.Interaction, difficulty: Choice[int], id: int, language: Choice[str]):
    if os.name == "nt":
        # only windows doesn't support bash commands
        await interaction.response.send_message("VeryUsefulBot伺服器運行在Windows上，暫時無法使用此功能。")
        return
    file_path = f"assets/code_test/{difficulty.value}/{id}.json"
    if os.path.exists(file_path):
       global id_global, lang
       id_global = [difficulty.value, id]
       lang = language.value
       await interaction.response.send_modal(SubmitWindow())
    else:
        await interaction.response.send_message(f"抱歉，難易度 {diffToName(difficulty.value)} 的 id{id} 不存在", ephemeral=True)
    

    file = discord.ui.TextInput(
        style=discord.TextStyle.paragraph,
        label="題目JSON檔",
        required=True,
        placeholder="請輸入產生的題目JSON檔"
    )

    async def on_submit(self, interaction: discord.Interaction):
        # Yeah this code sucks but works

        to_check: dict = json.loads(self.file.value)
        # Check if every key exists
        standard = ["name", "from", "difficulty", "question", "input_format", "output_format", "examples", "tests"].sort()
        every_key = [key for key in to_check.keys()].sort()
        if every_key != standard:
            await interaction.response.send_message("你的輸入有誤，請檢查後再試一次 (缺少項目)")
            return
        # Check if difficulty is valid
        if to_check["difficulty"] not in [0,1,2,3,4]:
            await interaction.response.send_message("你的輸入有誤，請檢查後再試一次 (difficulty)")
            return
        # Too lazy to check if the examples and tests are valid
        # Maybe I'll do it later :)
        
        # save the file
        difficulty = to_check["difficulty"]
        with open(f"assets/code_test/{difficulty}/last_id.txt", "r") as f:
            last_id = int(str(f.read()))
        last_id += 1
        with open(f"assets/code_test/{difficulty}/last_id.txt", "w") as f:
            f.write(str(last_id))
        with open(f"assets/code_test/{difficulty}/{last_id}.json", "w") as f:
            f.write(json.dumps(to_check, indent=4, ensure_ascii=False))
            
        await interaction.response.send_message(f"已新增題目，你的題目id是`{last_id}` (`{diffToName(difficulty)}`)")

            
    async def on_error(self, interaction: discord.Interaction, error):
        print(error)  # prints error 