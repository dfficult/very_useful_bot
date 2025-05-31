# `/option`指令

`/option`指令可以用來改變個人偏好設定，不會影響到其他人的設定。
這些設定主要為視覺方面的調整。

以下設定可供更改
- [`WordleBackgroundColor`]()
- [`WordleBlockMargin`]()
- [`WordleBlockSize`]()
- [`WordleFontColor`]()
- [`WordleGrayColor`]()
- [`WordleGreenColor`]()
- [`WordleImageMargin`]()
- [`WordleYellowColor`]()


### WordleAttemps - 更改Wordle猜測次數
你可以改變Wordle猜測次數，以獲得更多次機會
類別: `int`
範圍: `2~10`
預設: `6`


### WordleBackgroundColor - 變更Wordle背景顏色
你可以透過改變Wordle背景顏色來符合Discord主題的背景顏色，讓Wordle圖片看起來沒有邊框。
類別: `str`
預設: `#2e2e34`
> `#070709`:  Onyx Theme (條紋晶體主題)
> `#1a1a1e`:  Dark Theme (灰暗主題)
> `#2e2e34`:  Ash Theme (預設灰暗主題)
> `#fbfbfb`:  Light Theme (明亮主題)


### WordleBlockSize - 變更Wordle每格字母大小
你可以改變Wordle每格字母大小，這同時會影響字型大小。
類別: `int`
預設: `50`


### WordleBlockargin - 變更Wordle每格之間的間距
你可以改變Wordle每格之間的間距。
類別: `int`
預設: `5`


### WordleFontColor - 變更Wordle文字的顏色
你可以改變Wordle文字的顏色，以符合你的方塊顏色。
類別: `str`
預設: `#ffffff`


### WordleGrayColor - 變更Wordle猜測錯誤的顏色
你可以改變Wordle猜測錯誤的顏色(灰色)。
類別: `str`
預設: `#3a3a3c`


### WordleGreenColor - 變更Wordle位置正確的顏色
你可以改變Wordle猜測錯誤的顏色(綠色)。
類別: `str`
預設: `#538d4e`


### WordleImageMarginRight - 變更Wordle圖片右邊界 (尚未實裝)
部分裝置上可能無法一次顯示5個字母，可以透過此指令更改圖片右邊框厚度
類別: `int`
預設: `0`


### WordleYellowColor - 變更Wordle位置錯誤的顏色
你可以改變Wordle猜測錯誤的顏色(黃色)。
類別: `str`
預設: `#b59f3b`




