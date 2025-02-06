# very_useful_bot
[v1.6 Beta 1.1](#changelog)  
2025.2.7  

如同名稱，這是一個非常有用的Discord機器人，以下是主打的功能：

- ### Wordle
    最好玩的Wordle遊戲現在在Discord上就能玩，而且一天可以玩無限次

- ### C++ Online Judge (線上解題系統)
    一個在Discord上的OJ系統，目前只支援C++

- ### 數學計算
    解決一些高中數學，例如約分分數、行列式、向量的內外積等。

- ### 吃什麼
    選出下一餐吃什麼。

- ### 單字卡
    複習單字的小工具。



## 安裝說明
> 執行環境：Linux  
> 需可執行 `gcc` 和 `g++`，才可以使用OJ系統  

```bash
# 下載 VeryUsefulBot
git clone https://github.com/dfficult/very_useful_bot
# 安裝額外的 module
pip3 install discord # Discord模組
pip3 install pillow  # 使用裡面的PIL模組用於Wordle繪製結果
# 輸入 Token
cd very_useful_bot/dc_bot/
nano token.txt       # 然後輸入你的 TOKEN
# 執行
python3 main.py
```

## 所有指令說明
( 沒有連結的代表說明還沒寫好 )  
VeryUsefulBot採用斜線指令(Slash Command) `/`，只要輸入 `/`，就有簡易的指令說明  
輸入`/vubhelp`會產生Github連結，導向這個頁面

### Wordle
`/wordle`

### 計算機
`/calculator`

### 單字卡
`/flashcard`

### 隨機
[`/eat`](manual/eat.md/#eat) `/addfood` [`dice`](manual/math.md/#dice-faces) [`/rand`](manual/math.md/#rand-items)

### 日期
`/daysleft` [`/today`](manual/others.md/#today)

### 提醒
[`/notice`](manual/notice.md/#notice) `/delnotice`

### OJ
`/code` [`/new_code_q`](manual/oj_create.md) `/submit_code`

### 數學
`/average` `/c` `/correlation` `/det2` `/det3` `/factorize` `/invrmtx2` `/p` `/simfrac` `/solve21` `/solve31` `/surface` `/vector` `/vectorl`

### 記帳 (**即將被提醒取代**)
[`/mdelete`](manual/money.md/#mdelete-option) [`/mhistory`](manual/money.md/#mhistory) [`/mlend`](manual/money.md/#mborrow-user-amount)


## Changelog

Latest: 1.6 Beta 1.1

### v1.6 Notice Update
- [1.6 Beta 1.1]() Removed `runcode.sh`
- [1.6 Beta 1](https://github.com/dfficult/very_useful_bot/commit/0b451bfbc8d80d88682abdf2cc80a6255d0e7c29) Token is now a seperate file, Reorganized all the files (Put data in `assets` folder, renamed `codes.py` to `oj.py`)

### v1.5 FlashCard, Wordle, and Calculator
- [1.5.3.01](https://github.com/dfficult/very_useful_bot/commit/ebe4429aee3f8b719e3b20cbeb88e701b7b62a43) Wordle: Fixed sometimes it does not show image properly
- [1.5.3](https://github.com/dfficult/very_useful_bot/commit/21a99691a45973f0b107d16f751268cd2f1f1ce4) Wordle: Edit message instead of creating a new message on every guess, Debug Mode set to ephemeral, Changed some variable to constant, Deletes message after 2 seconds, Added allowed guesses list
- [1.5.2.02](https://github.com/dfficult/very_useful_bot/commit/1d2e5f2fe09f9ac37c191c8a4fe95f5ec3d55d16) Fixed incorrect bottom color showing, made better debug mode, updated [readme.md](#very_useful_bot), added changelog
- [1.5.2.01](https://github.com/dfficult/very_useful_bot/commit/251297706200472cac2c86b7f59cd9faca392d73) Fixed winnig at 6th attempt returned lose
- [1.5.2](https://github.com/dfficult/very_useful_bot/commit/f637fd0beaff57ef169b897cebe626f3e623d7ba) Added Wordle
- [1.5.1](https://github.com/dfficult/very_useful_bot/commit/2c266c7dbe273a4024ec436c6f4166b30ca15cd6) Added Calculator
- [1.5.0.01](https://github.com/dfficult/very_useful_bot/commit/4c0967b52e9b8db868673ae6008c1ee8d64f0456) Updated readme.md (Forgot)
- [1.5.0](https://github.com/dfficult/very_useful_bot/commit/3cefe82fe8de5bd4ddfbd8f399121f33c0fe90e0) Added Flashcard, started adding version properly

### v1.4 OJ Update
- [1.4.3](https://github.com/dfficult/very_useful_bot/commit/4afcf33c5d91dc77e4d2224b04974a1692899f78) Fixed '\n' and ' ' evaluation of the code output
- [1.4.2](https://github.com/dfficult/very_useful_bot/commit/2c06455b2d24384ea21aa4472793c95199beed7d) Fixed file reading
- [1.4.1.01](https://github.com/dfficult/very_useful_bot/commit/4d6215d7050412a53413f10570a5ef1cbfac91e3) Fixed oj_create.md
- [1.4.1](https://github.com/dfficult/very_useful_bot/commit/25a511afea089d79ba3e2103b160afe8918a0a1e) Removed one difficulty as it causes confusion, fixed missing last_id
- [1.4.0](https://github.com/dfficult/very_useful_bot/commit/bfc110815fe3ae92b06328262ed4fe301ce2aac9) Added difficulty, added new code adding support

### v1.3 Eat Command Update
- [1.3.1](https://github.com/dfficult/very_useful_bot/commit/88184e013a0a7c9e560f802bbd3d05b9590b1ced) Correct File location
- [1.3.02](https://github.com/dfficult/very_useful_bot/commit/d222ad4f90e52aa012505687a04ae7b51c0c1ed0) Removed wrong file
- [1.3.01](https://github.com/dfficult/very_useful_bot/commit/ee4710d136803f2c6a9df2153f0519588816ae2f) Removed wrong file
- [1.3.0](https://github.com/dfficult/very_useful_bot/commit/5289ac19a157eb6867fb0887963b92e6b86d6478) Fixed bot.change_presence not working, 
updated /eat by adding amount so you don't have to type the command 30 times

### v1.2 OJ and Notice
- [1.2](https://github.com/dfficult/very_useful_bot/commit/4608b547e9dd04fb66aa9e74a523c95d7570c00a) Added OJ and Notice, removed `__pychche__`, removed yazy game

### v1.1 Some Commands Update

- [1.1.2](https://github.com/dfficult/very_useful_bot/commit/46ff362da81c198268b4db6defacbdab017cb199) Added solve31, solve21, factorial commands

- [1.1.1](https://github.com/dfficult/very_useful_bot/commit/dade39e5ea98ed2254146d5044f303392aa9f37e) Removed drop down menu test file

- [1.1.0](https://github.com/dfficult/very_useful_bot/commit/0c3f8782435a7c9118399b1b6c6a8a254f56eada) Added today and vectorl command

### v1.0 Initial Commit
- [1.1](https://github.com/dfficult/very_useful_bot/commit/fd4d1b2cea2580cf75ce1eb9576a25a0e0b01ef0) Removed README.md generated by GitHub because my [readme.md](#very_useful_bot) exists
- [v1](https://github.com/dfficult/very_useful_bot/commit/58cbbdc727c8fb132622094c79042119ebf32742#diff-5a831ea67cf5cf8703b0de46901ab25bd191f56b320053be9332d9a3b0d01d15) Added pretty much everything to [GitHub](https://github.com/dfficult/very_useful_bot)
- [v0](https://github.com/dfficult/very_useful_bot/commit/853c6eb2668d09d40497a7cfc83d37ae593354f5) Initial Commit