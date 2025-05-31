# 記住誰欠你多少錢
> 別人欠你多少錢都不知道? 簡單紀錄你借出去多少錢。

共有3個指令  
1. [`/mborrow` 紀錄誰欠你錢](#mborrow)
2. [`/mhistory` 查看誰欠你錢](#mhistory)
3. [`/mdelete` 刪除紀錄](#mdelete)


---
#### `/mborrow <user> <amount>`
**紀錄誰欠你錢。**  
(指令提示：紀錄誰欠你錢)
> `user: discord.User` 輸入欠你錢的人 (@...)  
> `amount: int` 輸入金額 (正整數，不用加上$或單位)

本指令會讀取與寫入[money.json](/dc_bot/money.json)。  
我懶得用database，所以簡單的用一個json檔來儲存所有人的紀錄。

範例：`/mborrow user:@VeryUsefulBot amount:100`
> #### 紀錄儲存成功!
> VeryUsefulBot#1234欠你100  
> 今天 16:00


---
#### `/mhistory`
**列出你借錢出去的紀錄，查看誰欠你錢。**  
(指令提示：查看誰欠你錢)
> 本指令不需要任何參數。  

本指令會讀取[money.json](/dc_bot/money.json)，然後列出你借錢出去的紀錄。  
以下範例中，`user`會是你的id

範例：`/mhistory`
> #### user借錢出去的紀錄
> 共1筆紀錄，金額總和100元  
> `[1] VeryUsefulBot#1234欠你100` 2024/4/31 16:00


---
#### `/mdelete <option>`
**刪除紀錄。**  
(指令提示：刪除紀錄)
> `option: int` 編號 (使用 [/mhistory] 來查看紀錄編號)

本指令會讀取與寫入[money.json](/dc_bot/money.json)。 

範例：`/mdelete option:1`
```
紀錄刪除成功
```