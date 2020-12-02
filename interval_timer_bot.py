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
    await context.send('Hello there!')


@bot.command(name='start-timer', help='Starts a timer with a specified configuration.')
async def start_timer(context, repetitions: int, work: int, rest: int):
    global timer
    if timer is not None:
        await context.send('There is already an active timer, please stop it first.')
    else:
        timer = IntervalTimer(repetitions, work, rest)
        VoiceAnnouncer(context, timer)
        timer.start()
        await context.send(f'Alright, {repetitions} repetitions of {work} seconds work and {rest} seconds break, comin\' right up!')


@bot.command(name='stop-timer', help='Stops the timer currently running.')
async def stop_timer(context):
    global timer
    if timer is not None:
        timer.stop()
        await context.send('The timer was stopped.')
    else:
        await context.send('There was no timer to stop, but let\'s still call this a success, shall we?')


@bot.command(name='join-voice', help='Instructs the bot to join the voice channel you are in.')
async def join_voice(context: commands.Context):
    # Not sure how to do this nicely, in other languages I would use the null-conditional operator on voice
    voice_channel = context.author.voice.channel if context.author.voice is not None else None
    
    if voice_channel is None:
        await context.send('Oh my, I do not know where to go. Please join a voice channel so I can follow you.')
        return
    
    voice_client = await voice_channel.connect()
    voice_client.play(discord.FFmpegPCMAudio('sounds/beep.mp3'))


@bot.command(name='leave-voice', help='Instructs the bot to leave its voice channel.')
async def leave_voice(context: commands.Context):
    await context.voice_client.disconnect()



bot.run(os.getenv('BOT_TOKEN'))
