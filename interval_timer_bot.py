from dotenv import load_dotenv
load_dotenv()

import os
import asyncio
import discord
from discord.ext import commands

from interval_timer import IntervalTimer
from voice_announcer import VoiceAnnouncer


bot = commands.Bot(command_prefix='!')
timer = None

@bot.event
async def on_ready():
    print(f'The bot has logged in as {bot.user} and is ready to serve requests of its human overlords.')

@bot.command(name='hello', help='Responds with a hello message to show bot is up.')
async def greeting(context):
    await context.send('Hi there!')

@bot.command(name='start', help='Starts a timer with a specified configuration.')
async def start_timer(context, repetitions: int, work: int, rest: int):
    global timer
    if timer is not None:
        await context.send('There is already an active timer, please stop it first.')
    else:
        timer = IntervalTimer(repetitions, work, rest)
        VoiceAnnouncer(context, timer)
        timer.start()
        await context.send(f'{repetitions} repetitions of {work} seconds work and {rest} seconds break, comin\' right up!')
    
@bot.command(name='stop', help='Stops the timer currently running.')
async def stop_timer(context):
    global timer
    if timer is not None:
        timer.stop()
        await context.send('The timer was stopped.')
    else:
        await context.send('There was no timer to stop, but let\'s still call this a success?')


bot.run(os.getenv('BOT_TOKEN'))
