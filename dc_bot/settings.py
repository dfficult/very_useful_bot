"""
This settings file store bot's settings
import settings and access by settings.xxx
"""
import discord

Version = "1.8.1"
LANG = "zh_TW"
class Colors:
    notice = discord.Color.dark_magenta()
    food = discord.Color.gold()
    math = discord.Color.lighter_gray()
    wordle = discord.Color.teal()
    flashcard = discord.Color.magenta()
    oj = discord.Color.yellow()
    money = discord.Color.fuchsia()
    fail = discord.Color.red()
    success = discord.Color.green()
class Activity:
    content = "WWDC 2025 — June 9 | Apple"
    doing = "watching"  # watching, playing, listening
    