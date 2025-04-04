# 新增題目json檔

每一題題目都會存在一個`json`檔裡面，在這篇教學，你會了解如何生成一個題目json檔

你有兩種方法：
1. [使用題目新增器 (Comming soon)](#方法一)
2. [手動建立題目json檔](#方法二)


## 方法一
**使用題目新增器 (Comming soon)**  
對，Comming Soon，我還沒做好，請前往[方法二](#方法二)


## 方法二
**手動建立題目json檔**  
這個方法比較繁複，但你都決定要往下看了，就做吧

### 範例
先來看一個完整檔案的範例：
```json
{
    "name": "線性變換",
    "difficulty": 0,
    "from": "Dfficult",
    "question": "給定一個二階線性變換矩陣A和一個平面向量V，求出向量V線性變換後的向量",
    "input_format": "第一行，有四個數a11, a12, a21, a22，aij代表矩陣A的第i列第j行\n第二行有兩個數x和y，為向量V的x和y座標\n數值皆小於10^6",
    "output_format": "輸出向量V線性變換後的向量，以空格隔開x和y值",
    "examples": [
        {
            "input": "1 2 3 4\n5 6",
            "output": "17 39"
        },
        {
            "input":"0 1 -1 0\n2024 2025",
            "output": "2025 -2024"
        }
    ],
    "tests": [
        {
            "input": "9 8 7 6\n5 4",
            "output": "77 59"
        },
        {
            "input":"0 0 0 0\n98765 43210",
            "output": "0 0"
        },
        {
            "input": "314 159 265 358\n979 323",
            "output":"358763 375069"
        },
        {
            "input": "1 0 0 1\n 999999 999999",
            "output":"999999 999999"
        }
    ]

}
```
呈現結果：

> **#0001**  
> **線性變換**  
> 給定一個二階線性變換矩陣A和一個平面向量V，求出向量V線性變換後的向量   
> **輸入格式**  
> 第一行，有四個數a11, a12, a21, a22，aij代表矩陣A的第i列第j行  
> 第二行有兩個數x和y，為向量V的x和y座標  
> 數值皆小於10^6  
> **輸出格式**  
> 輸出向量V線性變換後的向量，以空格隔開x和y值  
> **範例輸入1**  
> 1 2 3 4  
> 5 6  
> **範例輸出1**  
> 17 39  
> **範例輸入2**  
> 0 1 -1 0  
> 2024 2025  
> **範例輸出2**  
> 2025 -2024  
> **提交程式碼**  
> 使用 `/submit_code id:0001` 來開啟輸入視窗  
> 語言：C/C++  
> 記憶體限制：256MB  
> 難易度：簡單 | 來源：Dfficult  

### 模板
由[以上範例](#範例)可以看出結構大致為：
```json
{
    "name": "題目名稱",
    "difficulty": 0,
    "from": "題目來源",
    "question": "題目",
    "input_format": "輸入格式說明",
    "output_format": "輸出格式說明",
    "examples": [
        {
            "input": "範例輸入1",
            "output": "範例輸出1"
        },
        {
            "input":"範例輸入2",
            "output": "範例輸出2"
        }
    ],
    "tests": [
        {
            "input": "測試資料1",
            "output": "正確輸出1"
        },
        {
            "input":"測試資料2",
            "output": "正確輸出2"
        },
        {
            "input": "測試資料3",
            "output":"正確輸出3"
        },
        {
            "input": "測試資料4",
            "output":"正確輸出4"
        }
    ]

}
```
你可以複製[此模板](#模板)，填入自己想要的題目

### 說明
以下是特別說明：
1. 使用 `\n` 表換行
2. `difficlty` 代表題目難易度，請輸入**0~2的整數(int)**：
    > `0`：簡單，那種基本四則運算或輸入輸出  
    > `1`：普通，放一些普通的題目  
    > `2`：困難，大概是APCS的實作的後兩題那種
3. 除了 `difficlty`，其他都請輸入文字(str)