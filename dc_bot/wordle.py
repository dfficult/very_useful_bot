import discord
from discord import app_commands, File
from PIL import Image, ImageDraw, ImageFont
import random, io


class Wordle:
    def __init__(self, player, answer):
        self.player = player
        self.guesses = []
        self.color = []
        self.answer = answer
        self.correct = []
        self.wrong_place = []
        self.incorrect = []
        self.left = [chr(i) for i in range(ord('A'), ord('Z')+1)] # A to Z
    
    def guess(self, guess: str) -> int:
        """
        Returns 0 when you still have chances.
        Returns 1 when you win.
        Returns 2 when you lost all chances.
        """
        result = [()] * 5
        
        # Track every letter occurence in answer
        answer_letter_count = {}
        for i in self.answer:
            answer_letter_count[i] = answer_letter_count.get(i, 0) + 1


        # green
        self.correct = []
        for i in range(len(guess)):
            if guess[i] == self.answer[i]:
                result[i] = (83, 141, 78) # rgb green
                answer_letter_count[guess[i]] -= 1
                # add to self.correct
                if guess[i] not in self.correct:
                    self.correct.append(guess[i])
                    bubble_sort(self.correct)
                # remove from self.wrong_place
                if guess[i] in self.wrong_place: self.wrong_place.remove(guess[i])
                # remove from self.incorrect
                if guess[i] in self.incorrect: self.incorrect.remove(guess[i])
                # remove from self.left
                if guess[i] in self.left: self.left.remove(guess[i])

        # yellow / gray
        self.wrong_place = []
        for i in range(len(guess)):
            if result[i] != (83, 141, 78): # not green
                # yellow
                if guess[i] in self.answer and answer_letter_count[guess[i]] > 0:
                    result[i] = (181, 159, 59) # rgb yellow
                    answer_letter_count[guess[i]] -= 1
                    # add to self.wrong_place
                    if guess[i] not in self.wrong_place:
                        self.wrong_place.append(guess[i])
                        bubble_sort(self.correct)
                    # remove from self.incorrect
                    if guess[i] in self.incorrect: self.incorrect.remove(guess[i])
                    # remove from self.left
                    if guess[i] in self.left: self.left.remove(guess[i])
                # gray
                else:
                    result[i] = (58, 58, 60) # rgb gray
                    if guess[i] in self.correct or guess[i] in self.wrong_place: continue
                    # add to self.incorrect
                    if guess[i] not in self.incorrect: self.incorrect.append(guess[i])
                    # remove from self.left
                    if guess[i] in self.left: self.left.remove(guess[i])

        self.color.append(result)
        self.guesses.append([i for i in guess])
        
        if len(self.guesses) >= 6:
            return 2 # lose
        elif guess == self.answer:
            return 1 # win
        else:
            return 0


playerdata = []

def turn_lower_to_upper(word: str) -> str:
    """
    Turns lowercase letter to upper case.
    Example: "hello" returns "HELLO". 
    Return SyntaxError when word is not A~Z or a~z.
    """
    result = ""
    for i in range(len(word)):
        ascii_value = ord(word[i])
        if ascii_value >= 65 and ascii_value <= 90: # A~Z
            result += chr(ascii_value)
        elif ascii_value >= 97 and ascii_value <= 122: # a~z
            result += chr(ascii_value - 32)
        else:
            raise SyntaxError("Not English")
    return result

def bubble_sort(to_sort: list) -> None:
    """
    Bubble sorts a list.
    """
    for i in range(len(to_sort)):
        swapped = False
        for j in range(0, len(to_sort)-i-1):
            if to_sort[j] > to_sort[j+1]:
                to_sort[j], to_sort[j+1] = to_sort[j+1], to_sort[j]
                swapped = True
        if not swapped: break




@app_commands.command(name="wordle", description="[Worlde] 猜測Wordle單字")
@app_commands.describe(guess="你的猜測")
async def wordle(interaction: discord.Interaction, guess: str):
    
    # Wordlist
    # taken from here: https://gist.github.com/cfreshman/a03ef2cba789d8cf00c08f767e0fad7b
    with open("wordle.txt", "r") as f:
        wordlist = [i.strip() for i in f.readlines()]

    # Join game
    global playerdata
    find = False
    for i in playerdata:
        if i.player == interaction.user.name: find = True
        game = i
    if not find:
        # Randomly select an answer
        word = wordlist[random.randint(0, len(wordlist)-1)]
        answer = turn_lower_to_upper(word)
        game = Wordle(player = interaction.user.name, answer = answer)
        playerdata.append(game)

    
    # Evaluate the guess
    # Turn everything to upper
    try:
        guess = turn_lower_to_upper(guess)
    except SyntaxError:
        await interaction.response.send_message(f"{guess} 包含非英文字元")
        return
    # Stop game detection
    if guess == "STOP":
        # stop the game
        for i in range(len(playerdata)):
            if playerdata[i].player == interaction.user.name:
                playerdata.pop(i)
        await interaction.response.send_message(f"答案是{game.answer}，已關閉遊戲")
        return
    # Debug mode
    if guess == "DEBG":
        # debug only
        embed = discord.Embed(
            title="Debug Mode",
            description="For debug purpose only.",
            color=discord.Color.dark_red()
        )
        embed.add_field(name="player", value=game.player)
        embed.add_field(name="answer", value=game.answer)
        embed.add_field(name="correct", value=game.correct)
        embed.add_field(name="wrong_place", value=game.wrong_place)
        embed.add_field(name="incorrect", value=game.incorrect)
        embed.add_field(name="left", value=game.left)
        await interaction.response.send_message(embed=embed)
        return
    # Word length detection
    if len(guess) != 5:
        await interaction.response.send_message(f"{guess} 的長度不是5個字")
        return
    # Word not found detection
    if guess in wordlist:
        result = game.guess(guess)
    else:
        await interaction.response.send_message(f"{guess} 不在單字清單內")
        return


    # Draw image
    WIDTH = 50
    HEIGHT = 50
    MARGIN= 5
    WORD_LENGTH = 5
    ATTEMPS = 6
    # Fonts: for Windows, arial is there
    try: font = ImageFont.truetype("arial.ttf", 30)
    except: font = ImageFont.load_default()
    # Fonts: for Linux, ChatGPT told me to use this
    try: font = ImageFont.truetype(r"/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
    except: font = ImageFont.load_default()
    # Draw image
    image_width = (WIDTH + MARGIN) * WORD_LENGTH - MARGIN
    image_height = (HEIGHT + MARGIN) * ATTEMPS - MARGIN
    image = Image.new("RGB", (image_width, image_height), color=(46, 48, 53))
    draw = ImageDraw.Draw(image)
    for i in range(ATTEMPS):
        for j in range(WORD_LENGTH):
            x1 = j * (WIDTH + MARGIN)
            y1 = i * (HEIGHT + MARGIN)
            x2 = x1 + WIDTH
            y2 = y1 + HEIGHT
            try:
                color = game.color[i][j]
                text = game.guesses[i][j]
                draw.rectangle([x1, y1, x2, y2], fill=color)
                text_width, text_height = draw.textsize(text, font=font)
                text_x = x1 + (WIDTH - text_width) // 2
                text_y = y1 + (HEIGHT - text_height) // 2
                draw.text((text_x, text_y), text, fill=(255, 255, 255), font=font)
            except:
                draw.rectangle([x1, y1, x2, y2], fill=(58, 58, 60)) # gray
            
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')    
    buffer.seek(0) 


    # update playerdata
    for i in range(len(playerdata)):
        if playerdata[i].player == interaction.user.name:
            playerdata[i] = game

    # embed
    embed = discord.Embed(
        title=f"猜測 {len(game.guesses)}/6",
        description="",
        color=discord.Color.green()
    )
    

    # win/lose detection
    if result == 1:
        embed.description = "你贏了"
        for i in range(len(playerdata)):
            if playerdata[i].player == interaction.user.name:
                playerdata.pop(i)
    elif result == 2:
        embed.description = f"你輸了，正確答案是**{game.answer}**"
        for i in range(len(playerdata)):
            if playerdata[i].player == interaction.user.name:
                playerdata.pop(i)
    else:
        embed.add_field(name="位置正確", value="".join(i for i in game.correct))
        embed.add_field(name="位置錯誤", value="".join(i for i in game.wrong_place))
        embed.add_field(name="猜測錯誤", value="".join(i for i in game.incorrect))
        embed.add_field(name="尚未嘗試", value="".join(i for i in game.left))


    # send image
    await interaction.response.send_message(file=File(buffer, 'myimage.png'), embed=embed)

