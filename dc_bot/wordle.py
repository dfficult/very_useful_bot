import discord
from discord import app_commands, File
from PIL import Image, ImageDraw, ImageFont
import random, io, json
import settings


# Settings (DO NOT CHANGE, DIFFERENT VALUE HAVE NOT TESTED YET)
DELETE_AFTER = 2  # Invalid guess message deletes after x seconds
WORD_LENGTH = 5   # How long a word is (Note: wordle.txt need to all be this long or cause bug)
ATTEMPS = 6       # How many attempts a user can have



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


class Wordle:
    def __init__(self, player, answer):
        self.player = player     # player id
        self.msg = None          # the message to edit, update upon first guess message sending
        self.guesses = []        # store the guesses
        self.color = []          # store the colors in rgb format
        self.answer = answer     # the answer
        self.correct = []        # store the green letters
        self.wrong_place = []    # store the yellow letters
        self.incorrect = []      # store the gray letters
        self.left = [chr(i) for i in range(ord('A'), ord('Z')+1)] # A to Z
    
    def guess(self, guess: str) -> int:
        """
        Returns 0 when you still have chances.
        Returns 1 when you win.
        Returns 2 when you lost all chances.
        """
        result = [()] * WORD_LENGTH
        
        # Track every letter occurence in answer
        answer_letter_count = {}
        for i in self.answer:
            answer_letter_count[i] = answer_letter_count.get(i, 0) + 1


        # green
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
        
        if guess == self.answer:
            return 1 # win
        elif len(self.guesses) >= ATTEMPS:
            return 2 # lose
        else:
            return 0


playerdata = []


@app_commands.command(name="wordle", description="[Worlde] 猜測Wordle單字")
@app_commands.describe(guess="你的猜測")
async def wordle(interaction: discord.Interaction, guess: str):
    
    # Wordlist
    # Possible answers, taken from here: https://gist.github.com/cfreshman/a03ef2cba789d8cf00c08f767e0fad7b
    with open("assets/wordle/answers.txt", "r") as f:
        answer_list = [i.strip() for i in f.readlines()]
    # Allowed guesses (Seperated to prevent least seen words to be the answer), taken from here: https://gist.github.com/cfreshman/40608e78e83eb4e1d60b285eb7e9732f
    with open("assets/wordle/allowed_guesses.txt", "r") as f:
        allowed_guesses = [i.strip() for i in f.readlines()]
    # Join game
    global playerdata
    find = False
    for i in playerdata:
        if i.player == interaction.user.name:
            find = True
            game = i
            break
    if not find:
        # Randomly select an answer
        word = answer_list[random.randint(0, len(answer_list)-1)]
        answer = turn_lower_to_upper(word)
        game = Wordle(player = interaction.user.name, answer = answer)
        playerdata.append(game)

    
    # Evaluate the guess
    # Turn everything to upper
    try:
        guess = turn_lower_to_upper(guess)
    except SyntaxError:
        await interaction.response.send_message(f"{guess} 包含非英文字元", delete_after=DELETE_AFTER)
        return
    # Quit game detection
    if guess == "QUIT":
        # End the game
        playerdata = [i for i in playerdata if i.player != interaction.user.name]
        await interaction.response.send_message(f"答案是{game.answer}，已結束遊戲", delete_after=DELETE_AFTER)
        return
    # Word length detection
    if len(guess) != WORD_LENGTH:
        await interaction.response.send_message(f"{guess} 的長度不是{WORD_LENGTH}個字", delete_after=DELETE_AFTER)
        return
    # Word not found detection
    if guess in answer_list or guess in allowed_guesses:
        result = game.guess(guess)
    else:
        await interaction.response.send_message(f"{guess} 不在單字清單內", delete_after=DELETE_AFTER)
        return


    # Draw image
    WIDTH = 50
    HEIGHT = 50
    MARGIN= 5
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


    # Update playerdata
    for i in range(len(playerdata)):
        if playerdata[i].player == interaction.user.name:
            playerdata[i] = game

    # Embed
    embed = discord.Embed(
        title=f"猜測 {len(game.guesses)}/{ATTEMPS}",
        description="",
        color=settings.Colors.wordle
    )
    

    # Win/Lose Detection
    if result not in [1, 2]:
        # Not win or lose, continue the game
        if len([i for i in game.correct]) != 0:
            embed.add_field(name="位置正確", value="".join(i for i in game.correct))
        if len([i for i in game.wrong_place]) != 0:
            embed.add_field(name="位置錯誤", value="".join(i for i in game.wrong_place))
        if len([i for i in game.incorrect]) != 0:
            embed.add_field(name="猜測錯誤", value="".join(i for i in game.incorrect))
        embed.add_field(name="尚未嘗試", value="".join(i for i in game.left))
    else:
        # result = 1: win
        # result = 2: lose
        embed.description = f"你輸了，答案為{game.answer}" if result-1 else "你贏了"
        embed.color = settings.Colors.fail if result-1 else settings.Colors.success
        
        # update stats
        with open("assets/stats.json", 'r') as f:
            stats = json.load(f)
        stats["wordle"]["times_played"] += 1
        try:
            player = stats["wordle"]["players"][f"{game.player}"]
            player["played"] += 1
        except:
            stats["wordle"]["players"].setdefault(f"{game.player}", {
                "played": 1,
                "win": 0,
                "lose": 0,
                "streak": 0
            })
            player = stats["wordle"]["players"][f"{game.player}"]
        if result == 1:  # win
            player["win"] += 1
            player["streak"] += 1
        else:            # lose
            player["lose"] += 1
            player["streak"] = 0
        
        # write back stats
        with open("assets/stats.json", "w") as f:
            f.write(json.dumps(stats, indent=4))

        # print stats
        embed.add_field(name="遊玩次數", value=player["played"])
        embed.add_field(name="獲勝次數", value=player["win"])
        embed.add_field(name="獲勝率", value=f"{round(player['win']/player['played']*100, 2)}%")
        embed.add_field(name="連勝次數", value=player["streak"])

        # remove player data from playerdata
        playerdata = [i for i in playerdata if i.player != interaction.user.name]
        

    # Send Results
    if len(game.guesses) == 1:
        await interaction.response.send_message(file=File(buffer, 'myimage.png'), embed=embed)
        message = await interaction.original_response()
        game.msg = message
    else:
        try:
            message = await game.msg.channel.fetch_message(game.msg.id)  # get message
            await message.edit(attachments=[File(buffer, 'myimage.png')], embed=embed)
            await interaction.response.send_message("已上傳猜測，請查看原始訊息", delete_after=DELETE_AFTER)
        except Exception as e:
            print(e)
            buffer.seek(0)  # Reset position again before trying to send the second time
            await interaction.response.send_message(f"發生錯誤 {e}，請回報此問題", file=File(buffer, 'myimage.png'), embed=embed)
            message = await interaction.original_response()
            game.msg = message
