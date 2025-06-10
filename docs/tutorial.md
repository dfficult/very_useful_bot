# 教學：開發 VeryUsefulBot
[VeryUsefulBot](https://github.com/dfficult/very_useful_bot) 是一款使用 Python 開發的 Discord 機器人，使用 [discord.py](https://github.com/Rapptz/discord.py), [pillow](https://github.com/python-pillow/Pillow) 等多個 Python 模組。本說明文件將說明 VeryUsefulBot的架構，以及簡易的開發說明。


> 本教學適用於 [1.8.0](https://github.com/dfficult/very_useful_bot/releases/tag/v1.8.0) 以上的版本，[1.6 Beta 1](https://github.com/dfficult/very_useful_bot/commit/0b451bfbc8d80d88682abdf2cc80a6255d0e7c29) ~ [1.7.2](https://github.com/dfficult/very_useful_bot/commit/690776a64e3a1626e403e800213d740e314c85c4) 以及 [1.0](https://github.com/dfficult/very_useful_bot/commit/58cbbdc727c8fb132622094c79042119ebf32742) ~ [1.5.3.01](https://github.com/dfficult/very_useful_bot/commit/ebe4429aee3f8b719e3b20cbeb88e701b7b62a43) 的版本並未使用 Cog 架構，不適用此篇說明。

### 目錄
- [程式架構](#程式架構)
- [載入所有指令模組](#載入所有指令模組)
- [語言檔案與VeryUsefulBot設定](#語言檔案與veryusefulbot設定)
- [開發模組](#開發模組)



## 程式架構
VeryUsefulBot ([1.8.0](https://github.com/dfficult/very_useful_bot/releases/tag/v1.8.0)+) 的程式架構如下：
- [`dc_bot`](../dc_bot/) 所有程式
  - [`assets`](../dc_bot/assets/) 存放資料
    - [`code_test`]() 存放程式系統題目
    - [`expenses`]() 存放記帳系統資料
    - [`flashcard`]() 存放單字卡資料
    - [`lang`]() 存放語言檔案
    - [`run_code`]() 存放語言檔案
    - [`user_options`]() 存放語言檔案
    - [`wordle`]() 存放語言檔案
    - [`foodlist.txt`]() 存放語言檔案
    - [`notice.json`]() 存放語言檔案
    - [`stats.json`]() 存放語言檔案
  - [`cogs`](../dc_bot/cogs) 存放指令模組
    - [`eat.py`](../dc_bot/cogs/eat.py) 隨機抽取食物
    - [`flashcard.py`](../dc_bot/cogs/flashcard.py) 單字卡
    - [`gamble.py`](../dc_bot/cogs/gamble.py) 賭博小遊戲
    - [`money_tracker.py`](../dc_bot/cogs/money_tracker.py) 記帳系統
    - [`notice.py`](../dc_bot/cogs/notice.py) 提醒
    - [`oj.py`](../dc_bot/cogs/oj.py) 程式系統
    - [`quotify.py`](../dc_bot/cogs/quotify.py) 文字轉引言圖片
    - [`tools.py`](../dc_bot/cogs/tools.py) 實用的小工具
    - [`user_options.py`](../dc_bot/cogs/user_options.py) 更改使用者個別設定
    - [`vub_math.py`](../dc_bot/cogs/vub_math.py) 數學計算
    - [`wordle.py`](../dc_bot/cogs/wordle.py) Wordle 遊戲
  - [`lang.py`](../dc_bot/lang.py) 載入語言的程式
  - [`main.py`](../dc_bot/main.py) 主程式
  - [`math_module.py`](../dc_bot/math_module.py) 自訂數學模組
  - [`settings.py`](../dc_bot/settings.py) 載入機器人設定
  - [`token.txt`](../dc_bot/token.txt) 存放 Token
- [`docs`](../docs) 存放使用說明

## 載入所有指令模組

### 運行 VeryUsefulBot
主程式為 [`main.py`](../dc_bot/main.py)，要運行 VeryUsefulBot 程式時，請在 [`dc_bot`](../dc_bot/) 目錄下運行指令：

Windows
```bat
python main.py
```
Linux / macOS
```bash
python3 main.py
```

---

### main.py 在做什麼?

運行此檔案時會先讀取 [`token.txt`](../dc_bot/token.txt) 裡的內容，若該檔案無Token，程式會詢問你Token，並儲存進 [`token.txt`](../dc_bot/token.txt) 中。

接著會建立一個 Discord Bot 的 Instance。

然後讀取 [`cogs`](../dc_bot/cogs/) 資料夾內每一個 Python 檔案 ( 檔案後綴名為 `.py` )，若檔案可以被 Discord Cog 讀取，則程式將會載入該檔案；若載入失敗，則會顯示錯誤。

> 範例：在 Windows 上運行 [`main.py`](../dc_bot/main.py)，載入時會顯示以下訊息：
> ```bash
> 已載入擴充指令：notice.py
> 未載入擴充指令：oj.py
> 錯誤：Extension 'cogs.oj' raised an error: OSError: VeryUsefulBot伺服器運行在Windows上，暫時無法使用此功能。
> 已載入擴充指令：user_options.py
> 已載入擴充指令：flashcard.py
> 已載入擴充指令：eat.py
> 已載入擴充指令：wordle.py
> 已載入擴充指令：vub_math.py
> 已載入擴充指令：gamble.py
> 已載入擴充指令：money_tracker.py
> 已載入擴充指令：tools.py
> 已載入擴充指令：quotify.py
> 已載入 10 個擴充指令，未載入 1 個擴充指令
> VeryUsefulBot 已成功登入
> ```
最後，[`main.py`](../dc_bot/main.py) 會使用 Token 運行 Discord 機器人。

## 語言檔案與VeryUsefulBot設定

### 使用 text() 取得多語言文字

VeryUsefulBot 內所有顯示給使用者的訊息，皆透過 `lang.py` 提供的 `text()` 函式取得。這個函式會根據 [`settings.py`](../dc_bot/settings.py) 中的 `LANG` 參數，自動載入對應的語言檔（如 `zh_TW.json` 或 `en_US.json`），並回傳對應的文字內容。

#### 範例：取得指令描述

假設你在語言檔（如 `assets/lang/zh_TW.json`）中有以下內容：
```json
{
  "cmd.notice.description": "設定提醒"
}
```
你可以在 Cog 中這樣使用：
```python
from lang import *

@app_commands.command(name="notice", description=text("cmd.notice.description"))
async def notice(self, interaction: discord.Interaction):
    ...
```
如此一來，當你切換 `LANG` 設定，所有指令描述與訊息都會自動切換語言。

#### 新增語言

若要新增語言，只需在 `assets/lang/` 下新增對應語言的 JSON 檔案（如 `ja_JP.json`），並將 `settings.py` 的 `LANG` 改為對應語言代碼即可。 若指定語言檔不存在，系統會自動載入預設的 `zh_TW.json`。
 
新增文字時，只需在語言檔 JSON 裡新增對應 key-value 即可，程式會自動讀取。

---

### 設定檔與顏色

[`settings.py`](../dc_bot/settings.py) 提供機器人運作時的全域設定，例如顏色、語言、活動狀態等。你可以在這裡自訂機器人顯示的顏色主題，或修改預設語言。

#### 範例：自訂 embed 外框顏色

```python
class Colors:
    notice = discord.Color.dark_magenta()
    ...
```
在各個功能模組中，會直接引用這些顏色設定，例如：
```python
embed = discord.Embed(
    title="提醒",
    description="這是提醒內容",
    color=settings.Colors.notice
)
```


## 開發模組

要新增 VeryUsefulBot 的功能，請在 `dc_bot/cogs` 中建立一個 Python 檔案。

要作為 Cog 程式架構，需有一個名為 `setup()` 的 async 函式，參考如下：

```python
# 載入 Discord Module
import discord
from discord.ext import commands
from discord import app_commands

# 載入語言 Module
from lang import *

class YourClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 你的 Discord 斜線指令
    @app_commands.command(name="your_command", description=text("cmd.your_command.description"))
    async def your_command(self, interaction: discord.Interaction):
        await interaction.response.send_message("Hello World!")

# Setup() 告知主程式此為 Cog 檔案
async def setup(bot: commands.Bot):
    await bot.add_cog(YourClass(bot))
```


- [加入參數與描述](#加入參數與描述)
  - [加入選項](#加入選項)
  - [限制輸入範圍](#限制輸入範圍)
  - [非必填參數 (Optional)](#非必填參數-optional)
- [多個指令](#多個指令)
- [訊息右鍵選單](#訊息右鍵選單)
---

### 加入參數與描述

你可以使用 `@app_commands.describe` 來為指令參數加上說明，讓使用者在 Discord 介面上看到提示。例如：

```python
@app_commands.command(name="eat", description=text("cmd.eat.description"))
@app_commands.describe(amount=text("cmd.amount"))
async def eat(self, interaction: discord.Interaction, amount: int):
    ...
```
這樣在 Discord 斜線指令介面會顯示 `amount` 參數的說明。

- #### 加入選項
  你可以用 `@app_commands.choices` 讓參數有下拉選單，例如：

  ```python
  from discord.app_commands import Choice

  @app_commands.command(name="flashcard", description=text("cmd.flashcard.description"))
  @app_commands.choices(
      wordlist=[
          Choice(name="測試用單字卡", value="測試用單字卡.json")
      ]
  )
  async def flashcard(self, interaction: discord.Interaction, wordlist: Choice[str]):
      # 存取使用者選擇的值
      print(wordlist.name, wordlist.value)
      ...
  ```
- #### 限制輸入範圍
  你可以用 `Range[種類,最小值,最大值]` 讓參數有範圍，以下範例將n與k的範圍設為1~25。若使用者輸入不在範圍內的整數時，Discord 會阻止使用者送出該指令。
  
  ```python
  from discord.app_commands import Range

  @app_commands.command(name="p", description=text("cmd.p.description"))
  async def p(self, interaction: discord.Interaction, n: Range[int,1,25], k: Range[int,1,25]):
      ...
  ```
- #### 非必填參數 (Optional)
  你可以用 `Optional[種類]` 讓參數設定為非必填，例如：
    ```python
    from typing import Optional

    @app_commands.command(name="rand", description=text("cmd.rand.description"))
    async def rand(self, interaction: discord.Interaction, items: str, amount: Optional[int]):
      ...
    ```
---

### 多個指令

同一個 Cog 類別可以定義多個指令，只要在 class 內多加幾個 `@app_commands.command` 的 method 即可。例如：

```python
class Tools(commands.Cog):
    @app_commands.command(name="calculator", description=text("cmd.calculator.description"))
    async def calculator(self, interaction: discord.Interaction):
        ...

    @app_commands.command(name="daysleft", description=text("cmd.daysleft.description"))
    async def daysleft(self, interaction: discord.Interaction, date: str):
        ...
```

---

### 訊息右鍵選單

你可以用 `@app_commands.context_menu` 來建立訊息右鍵選單（Context Menu），讓使用者對訊息點右鍵時可以呼叫你的功能。特別注意的是，不用放進Class中。例如：

```python
@app_commands.context_menu(name=text("menu.wordcount"))
async def wordcount(interaction: discord.Interaction, message: discord.Message):
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
```

然後在 `setup()` 裡註冊這些 context menu：

```python
async def setup(bot: commands.Bot):
    await bot.add_cog(Tools(bot))
    bot.tree.add_command(wordcount)
```

---