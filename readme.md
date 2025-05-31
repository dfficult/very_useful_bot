# very_useful_bot
[v1.8.0](docs/changelog.md)  
2025.05.31  

VeryUsefulBot是一個非常有用的Discord機器人，以下是主打的功能：

- ### Wordle
    在Discord上就能玩的Wordle小遊戲，比起Discord上NyTimes的，這個一天可以玩無數次 

- ### C++ Online Judge (線上解題系統)
    一個在Discord上的OJ系統，目前只支援C和C++

- ### 數學計算
    解決一些簡單數學，例如約分分數、行列式、向量的內外積等。

- ### 記帳
    簡易的記帳系統。

- ### 單字卡
    複習單字的小工具。



## 安裝說明
> 運行環境：Linux, macOS, Windows等   
> **需可執行bash，且可執行 `gcc` 和 `g++`，才可以使用OJ系統**  

以可執行bash的系統為例：
```bash
# 下載 VeryUsefulBot
git clone https://github.com/dfficult/very_useful_bot

# 安裝額外的 module
pip3 install discord        # Discord模組
pip3 install pillow         # 使用裡面的PIL模組用於Wordle繪製結果

# 輸入 Token
cd very_useful_bot/dc_bot/  # 一定要在dc_bot目錄下運行
echo "MyToken" > token.txt  # 然後輸入你的 TOKEN

# 執行
python3 main.py
```

## 所有指令說明
( 沒有連結的代表說明還沒寫好 )  
VeryUsefulBot採用斜線指令(Slash Command) `/`，只要輸入 `/`，就有簡易的指令說明  

### 遊戲
[`/wordle`](manual/wordle.md) `/slot`

### 工具
`/calculator` `/daysleft`

### 單字卡
`/flashcard`

### 隨機
[`/eat`](manual/eat.md/#eat) `/addfood` [`/dice`](manual/math.md/#dice-faces) [`/rand`](manual/math.md/#rand-items)


### 提醒
[`/notice_after`](manual/notice.md/#notice) `/notice_at` `/notice_delete` `/note` `/notice_list`

### OJ
`/code` `/submit_code`

### 數學
`/average` `/c` `/common_deg_to_rad` `/correlation` `/det2` `/det3` `/factorize` `/invrmtx2` `/p` `/simfrac` `/solve21` `/solve31` `/surface` `/vector` `/vectorl` 

### 記帳
`/m_new_record` `/m_wallet`

### 其他
[`/option`](manual/options.md) `/quotify`
