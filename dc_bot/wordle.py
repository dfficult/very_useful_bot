import discord
from discord import app_commands, File
from PIL import Image, ImageDraw, ImageFont
import random, io, json, os
import settings, user_options
from lang import *

# Settings (DO NOT CHANGE, DIFFERENT VALUE HAVE NOT TESTED YET)
DELETE_AFTER = 2  # Invalid guess message deletes after x seconds
WORD_LENGTH = 5   # How long a word is (Note: wordle.txt need to all be this long or cause bug)
ATTEMPS = 6       # How many attempts a user can have



def turn_lower_to_upper(word: str) -> str:
    """
    Turns lowercase letter to upper case.\n
    Example: "hello" returns "HELLO".\n
    Return SyntaxError when word is not A ~ Z or a ~ z.\n
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

# GRAY = (58, 58, 60)
# YELLOW = (181, 159, 59)
# GREEN = (83, 141, 78)
# WHITE = (255, 255, 255)



class Wordle:
    def __init__(self, player, player_name, answer):
        self.player = player     # player id
        self.name = player_name  # player name
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
                result[i] = user_options.get_user_options(self.player, "WordleGreenColor")
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
            if result[i] != user_options.get_user_options(self.player, "WordleGreenColor"):
                # yellow
                if guess[i] in self.answer and answer_letter_count[guess[i]] > 0:
                    result[i] = user_options.get_user_options(self.player, "WordleYellowColor")
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
                    result[i] = user_options.get_user_options(self.player, "WordleGrayColor")
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

async def wordle_guess(interaction: discord.Interaction, guess: str):
    
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
        if i.player == interaction.user.id:
            find = True
            game = i
            break
    if not find:
        # Randomly select an answer
        word = answer_list[random.randint(0, len(answer_list)-1)]
        answer = turn_lower_to_upper(word)
        game = Wordle(player = interaction.user.id, player_name=interaction.user.name, answer = answer)
        playerdata.append(game)

    
    # Evaluate the guess
    # Turn everything to upper
    try:
        guess = turn_lower_to_upper(guess)
    except SyntaxError:
        await interaction.response.send_message(text("wordle.not_english"), delete_after=DELETE_AFTER)
        return
    # Quit game detection
    if guess == "QUIT":
        # End the game
        playerdata = [i for i in playerdata if i.player != interaction.user.id]
        await interaction.response.send_message(text("wordle.quit_game",game.answer), delete_after=DELETE_AFTER)
        return
    # Word length detection
    if len(guess) != WORD_LENGTH:
        if len(guess) >= 20: guess = guess[:20] + text("wordle.etc")
        await interaction.response.send_message(text("wordle.wrong_len",guess,WORD_LENGTH), delete_after=DELETE_AFTER)
        return
    # Word not found detection
    if guess in answer_list or guess in allowed_guesses:
        result = game.guess(guess)
    else:
        await interaction.response.send_message(text("wordle.not_in",guess), delete_after=DELETE_AFTER)
        return


    # Draw image

    # Get user options
    SIZE = user_options.get_user_options(interaction.user.id, "WordleBlockSize")
    MARGIN = user_options.get_user_options(interaction.user.id, "WordleBlockMargin")
    FONT_COLOR = user_options.get_user_options(interaction.user.id, "WordleFontColor")
    GRAY = user_options.get_user_options(interaction.user.id, "WordleGrayColor")
    BACKGROUND_COLOR = user_options.get_user_options(interaction.user.id, "WordleBackgroundColor")


    WIDTH = SIZE
    HEIGHT = SIZE
    FONT_SIZE = round(SIZE * 3 / 5)
    # Fonts: for Windows, arial is there
    try: font = ImageFont.truetype("arial.ttf", FONT_SIZE * 2)
    except: font = ImageFont.load_default()
    # Fonts: for Linux, ChatGPT told me to use this
    try: font = ImageFont.truetype(r"/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", FONT_SIZE)
    except: font = ImageFont.load_default()
    # Draw image
    image_width = (WIDTH + MARGIN) * WORD_LENGTH - MARGIN
    image_height = (HEIGHT + MARGIN) * ATTEMPS - MARGIN
    image = Image.new("RGB", (image_width, image_height), color=BACKGROUND_COLOR)
    draw = ImageDraw.Draw(image)
    for i in range(ATTEMPS):
        for j in range(WORD_LENGTH):
            x1 = j * (WIDTH + MARGIN)
            y1 = i * (HEIGHT + MARGIN)
            x2 = x1 + WIDTH
            y2 = y1 + HEIGHT
            try:
                color = game.color[i][j]
                txt = game.guesses[i][j]
                draw.rectangle([x1, y1, x2, y2], fill=color)
                # text_width, text_height = draw.textsize(text, font=font)
                bbox = font.getbbox(txt)
                txt_width = bbox[2] - bbox[0]
                txt_height = bbox[3] - bbox[1]
                txt_x = x1 + (WIDTH - txt_width) // 2
                txt_y = y1 + (HEIGHT - txt_height) // 2
                draw.text((txt_x, txt_y), txt, fill=FONT_COLOR, font=font)
            except:
                draw.rectangle([x1, y1, x2, y2], fill=GRAY)
            
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')    
    buffer.seek(0) 


    # Update playerdata
    for i in range(len(playerdata)):
        if playerdata[i].player == interaction.user.id:
            playerdata[i] = game

    # Embed
    embed = discord.Embed(
        title=text("wordle.guess",len(game.guesses),ATTEMPS),
        description="",
        color=settings.Colors.wordle
    )
    

    # Win/Lose Detection
    if result not in [1, 2]:
        # Not win or lose, continue the game
        if len([i for i in game.correct]) != 0:
            embed.add_field(name=text("wordle.correct"), value="".join(i for i in game.correct))
        if len([i for i in game.wrong_place]) != 0:
            embed.add_field(name=text("wordle.wrong_pos"), value="".join(i for i in game.wrong_place))
        if len([i for i in game.incorrect]) != 0:
            embed.add_field(name=text("wordle.incorrect"), value="".join(i for i in game.incorrect))
        embed.add_field(name=text("wordle.havent_tried"), value="".join(i for i in game.left))
    else:
        # result = 1: win
        # result = 2: lose
        embed.description = text("wordle.you_lose") if result-1 else text("wordle.you_win")
        embed.color = settings.Colors.fail if result-1 else settings.Colors.success
        
        # update stats
        with open("assets/stats.json", 'r') as f:
            stats = json.load(f)
        stats["wordle"]["times_played"] += 1
        try:
            player = stats["wordle"]["players"][f"{game.name}"]
            player["played"] += 1
        except:
            stats["wordle"]["players"].setdefault(f"{game.name}", {
                "played": 1,
                "win": 0,
                "lose": 0,
                "streak": 0
            })
            player = stats["wordle"]["players"][f"{game.name}"]
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
        embed.add_field(name=text("wordle.games_played"), value=player["played"])
        embed.add_field(name=text("wordle.games_won"), value=player["win"])
        embed.add_field(name=text("wordle.win_rate"), value=f"{round(player['win']/player['played']*100, 2)}%")
        embed.add_field(name=text("wordle.streak"), value=player["streak"])

        # remove player data from playerdata
        playerdata = [i for i in playerdata if i.player != interaction.user.id]
        

    # Send Results
    await interaction.response.send_message(file=File(buffer, f"Wordle guess {game.guesses}.png"), embed=embed)
    the_message = await interaction.original_response()
    if len(game.guesses) == 1:
        # Update game.msg
        game.msg = the_message
    else:
        # Not the first guess, remove the previous one
        try:
            # get message
            message = await game.msg.channel.fetch_message(game.msg.id)
            await message.delete()
        except Exception as e:
            print(e)
        finally:
            # Update game.msg
            game.msg = the_message 



@app_commands.command(name="wordle", description=text("cmd.wordle.description"))
@app_commands.describe(guess=text("cmd.wordle.guess"))
async def wordle(interaction: discord.Interaction, guess: str):
    await wordle_guess(interaction = interaction, guess = guess)



@app_commands.context_menu(name=text("menu.wordle"))
async def wordle_context_menu(interaction: discord.Interaction, message: discord.Message):
    await wordle_guess(interaction = interaction, guess = message.content)