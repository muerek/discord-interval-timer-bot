import asyncio
import discord

from interval_timer import IntervalTimer, TimerPhase


class VoiceAnnouncer():
    def __init__(self, voice_client: discord.VoiceClient):
        self._voice_client = voice_client

    def on_timer_tick(self, phase, done, remaining):
        print(f'Phase {phase} with {done} seconds done and {remaining} seconds remaining.')
        
        # Countdown is delivered as one audio file to avoid stuttering due to rate limiting, routing etc.
        if remaining == 3:
            # Note that this seems to be non-blocking without wrapping it into a task or alike.
            self._voice_client.play(discord.FFmpegPCMAudio('sounds/countdown.mp3'))

        if remaining == 5 and (phase == TimerPhase.Rest or phase == TimerPhase.Preparation):
            self._voice_client.play(discord.FFmpegPCMAudio('sounds/prepare.mp3'))

        # Play sound halfway through the work phase if it is 30 seconds or longer.
        if phase == TimerPhase.Work and remaining + done > 29:
            # We get ticks for every full second.
            # If work is set for an uneven amount of seconds, we cannot hit the exact half.
            # Play sound half a second earlier then.
            if done == remaining or done + 1 == remaining:
                self._voice_client.play(discord.FFmpegPCMAudio('sounds/bell.mp3'))

    def on_timer_started(self):
        self._voice_client.play(discord.FFmpegPCMAudio('sounds/timer-set.mp3'))

    def on_timer_ended(self):
        self._voice_client.play(discord.FFmpegPCMAudio('sounds/all-done.mp3'))

    def attach(self, timer: IntervalTimer):
        # Attach to the timer events.
        timer.started += self.on_timer_started
        timer.tick += self.on_timer_tick
        timer.ended += self.on_timer_ended

    def detach(self, timer: IntervalTimer):
        timer.started -= self.on_timer_started
        timer.tick -= self.on_timer_tick
        timer.ended -= self.on_timer_ended
