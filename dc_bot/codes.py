# === codes.py ===
import discord
from discord import app_commands
from discord.app_commands import Choice
from typing import Optional
import json, os, subprocess, random


# --- difficulty id to name ---
def diffToName(difficulty: int) -> str: 
    match difficulty:
        case 0: return "簡單"
        case 1: return "普通"
        case 2: return "中等"
        case 3: return "困難"



# --- SubmitWindow ---
class SubmitWindow(discord.ui.Modal, title="提交程式碼"):
    codes = discord.ui.TextInput(
        style=discord.TextStyle.paragraph,
        label="程式碼",
        required=True,
        placeholder="請輸入程式碼"
    )

    async def on_submit(self, interaction: discord.Interaction):
        # load the data about this test
        global id_global #[difficulty, id]
        with open(f"code_test/{id_global[0]}/{id_global[1]}.json", "r") as file:
           question = json.load(file)
        
        # prepare for discord embed
        embed = discord.Embed(
            title=f"{diffToName(id_global[0])} #{id_global[1]}",
            description="description",
            color=discord.Color.gold()
        )
        
        # save the code
        global lang
        codes = self.codes.value
        with open(f"test.{lang}", "w") as file:
            file.write(codes)

        # interaction must be sent within 3 seconds, so we need this
        await interaction.response.defer(thinking=True)

        # compile the code
        result = subprocess.run(["bash", f"run_code/compile_{lang}.sh"], capture_output=True, text=True)
        if result.stderr:
            # An error occurred
            embed.title = "Compile Error"
            embed.description = result.stderr
            embed.color = discord.Color.red()
            await interaction.followup.send(embed=embed)
            return

        # run code for every test data
        amount = len(question["tests"])
        passed = 0               # passed count
        errors = ["0"]*amount    # wrong output
        for i in range(amount):
            # load input data
            with open("input.txt", "w") as file:
                file.write(question["tests"][i]["input"])
            # let's run it
            runcode_path = f"run_code/run_{lang}.sh"
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
@app_commands.command(name="code", description="[OJ] 選擇程式題目")
@app_commands.describe(difficulty="難易度", id="指定題目編號 (若未指定，會隨機抽一個)")
@app_commands.choices(
    difficulty = [
        Choice(name="簡單", value=0),
        Choice(name="普通", value=1),
        Choice(name="中等", value=2),
        Choice(name="困難", value=3)
    ]
)
async def code(interaction: discord.Interaction, difficulty: Choice[int], id: Optional[int]):
    if not id:
        with open(f"code_test/{difficulty.value}/last_id.txt", "r") as f:
            id = random.randint(1,int(f.read()))
    file_path = f"code_test/{difficulty.value}/{id}.json"

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

        embed.add_field(name="提交程式碼", value=f"使用 `/submit_code difficulty:{diffToName(difficulty.value)} id:{id}` 來開啟輸入視窗\n語言：C/C++\n記憶體限制：256MB")
        embed.set_footer(text=f"來源：{question['from']}")
        embed.set_author(name=f"{diffToName(difficulty.value)} #{id}")

        await interaction.response.send_message(embed=embed)
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
        Choice(name="中等", value=2),
        Choice(name="困難", value=3)
    ]
)
async def submit_code(interaction: discord.Interaction, difficulty: Choice[int], id: int, language: Choice[str]):
    file_path = f"code_test/{difficulty.value}/{id}.json"
    if os.path.exists(file_path):
       global id_global, lang
       id_global = [difficulty.value, id]
       lang = language.value
       await interaction.response.send_modal(SubmitWindow())
    else:
        await interaction.response.send_message(f"抱歉，難易度 {diffToName(difficulty.value)} 的 id{id} 不存在", ephemeral=True)
    

# --- Command: new_code_q ---
@app_commands.command(name="new_code_q", description="[OJ] 新增題目")
async def new_code_q(interaction: discord.Interaction):
    await interaction.response.send_modal(NewCodeQWindow())


# --- NewCodeQWindow ---
class NewCodeQWindow(discord.ui.Modal, title="新增一個題目"):
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
        with open(f"code_test/{difficulty}/last_id.txt", "r") as f:
            last_id = int(str(f.read()))
        last_id += 1
        with open(f"code_test/{difficulty}/last_id.txt", "w") as f:
            f.write(str(last_id))
        with open(f"code_test/{difficulty}/{last_id}.json", "w") as f:
            f.write(json.dumps(to_check, indent=4, ensure_ascii=False))
            
        await interaction.response.send_message(f"已新增題目，你的題目id是`{last_id}` (`{diffToName(difficulty)}`)")

            
    async def on_error(self, interaction: discord.Interaction, error):
        print(error)  # prints error 