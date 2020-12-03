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
voice_announcer = None

@bot.event
async def on_ready():
    print(f'The bot has logged in as {bot.user} and is ready to serve requests of its human overlords.')


@bot.command(name='hello', help='Responds with a hello message to show bot is up.')
async def greeting(context):
    await context.send('Hello there!')


@bot.command(name='start-timer', help='Starts a timer with a specified configuration.')
async def start_timer(context, repetitions: int, work: int, rest: int):
    global timer, voice_announcer
    # We can only run one timer at the same time.
    if timer is not None:
        await context.send('There is already an active timer, please stop it first.')
        return
    
    timer = IntervalTimer(repetitions, work, rest)
    # Attach voice announcer to timer if it is set up.
    if voice_announcer is not None:
        voice_announcer.attach(timer)
    timer.start()
    
    await context.send(f'Alright, {repetitions} repetitions of {work} seconds work and {rest} seconds break, comin\' right up!')


@bot.command(name='stop-timer', help='Stops the timer currently running.')
async def stop_timer(context):
    global timer
    if timer is None:
        await context.send('There was no timer to stop, but let\'s still call this a success, shall we?')
        return
    timer.stop()
    voice_announcer.detach(timer)
    timer = None
    await context.send('The timer was stopped.')


@bot.command(name='join-voice', help='Instructs the bot to join the voice channel you are in.')
async def join_voice(context: commands.Context):
    # Not sure how to do this nicely, in other languages I would use the null-conditional operator on voice
    voice_channel = context.author.voice.channel if context.author.voice is not None else None
    
    if voice_channel is None:
        await context.send('Oh my, I do not know where to go. Please join a voice channel so I can follow you.')
        return
    
    voice_client = await voice_channel.connect()
    global voice_announcer
    voice_announcer = VoiceAnnouncer(voice_client)


@bot.command(name='leave-voice', help='Instructs the bot to leave its voice channel.')
async def leave_voice(context: commands.Context):
    global voice_announcer
    # TODO: Check if this actually kills the voice announcer or if it continues working
    voice_announcer = None
    await context.voice_client.disconnect()



bot.run(os.getenv('BOT_TOKEN'))
