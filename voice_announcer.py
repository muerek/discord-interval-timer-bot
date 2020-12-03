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

        if remaining == 5 and phase == TimerPhase.Rest:
            self._voice_client.play(discord.FFmpegPCMAudio('sounds/prepare.mp3'))

    def on_timer_started(self):
        print('Timer started.')

    def on_timer_ended(self):
        print('All done.')

    def attach(self, timer:IntervalTimer):
        # Attach to the timer events.
        timer.started += self.on_timer_started
        timer.tick += self.on_timer_tick
        timer.ended += self.on_timer_ended

    def detach(self, timer):
        timer.started -= self.on_timer_started
        timer.tick -= self.on_timer_tick
        timer.ended -= self.on_timer_ended
