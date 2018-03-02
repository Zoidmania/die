#!/usr/bin/python3
import configparser
import asyncio
import discord
from discord.ext import commands
import random, re, sys, six, os, click, pprint, operator
from math import ceil, floor
from collections import Counter


# Parse the config and stick in global "config" var.
config = configparser.ConfigParser()
for inifile in ['/home/zoidmania/die/die.ini']:
    if os.path.isfile(inifile):
        config.read(inifile)
        break  # First config file wins
MAIN = config['MAIN']


description = '''Dice tools bot.'''
bot = commands.Bot(command_prefix='die.', description=description)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def add(left : int, right : int):
    """Adds two numbers together."""
    await bot.say(left + right)

@bot.command()
async def sub(left : int, right : int):
    """Subtracts the right number from the left."""
    await bot.say(left - right)

@bot.command()
async def roll(dice : str):
    """Rolls a dice in NdN format.
The result will be sorted (ascending).
You may only roll up to 50 dice at once.
You may only roll up to a d100."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await bot.say('Format has to be in NdN!')
        return
    if limit > 100 or limit < 1:
        await bot.say('Die must have between 1 and 100 sides (inclusive)!')
        return
    if rolls > 50 or rolls < 1:
        await bot.say('Number of dice must be beteen 1 and 50 (includive)!')
        return

    await bot.say('Rolling {}d{}!'.format(rolls, limit))

    result = [random.randint(1, limit) for r in range(rolls)]
    result.sort()
    total = sum(result)
    avg_float = total / rolls
    if int(avg_float) == int(ceil(avg_float)):
        avg = int(avg_float)
    else:
        avg = int(floor(avg_float))
    med = result[rolls//2]
    counts = Counter(result)
    counts = sorted(counts.items(), key=operator.itemgetter(1))

    ans = ""
    ans += 'Individual dice values: ' + ', '.join(str(num) for num in result) + "\n"
    ans += 'Total: {}\n'.format(total)
    ans += 'Mean: {} (actual: {})\n'.format(avg, avg_float)
    ans += 'Median: {}\n'.format(med)
    ans += 'Counts:\n'
    for key, value in counts:
        ans += '    - {} was rolled {} times\n'.format(key, value)
    await bot.say(ans)

bot.run(MAIN.get('login_token'))
