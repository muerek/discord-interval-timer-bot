import asyncio
import discord

from interval_timer import IntervalTimer


class VoiceAnnouncer():
    def __init__(self, voice_client: discord.VoiceClient):
        self._voice_client = voice_client

    def on_timer_tick(self, phase, done, remaining):
        print(f'Phase {phase} with {done} seconds done and {remaining} seconds remaining.')
        if remaining == 0:
            self._voice_client.play(discord.FFmpegPCMAudio('sounds/beep.mp3'))

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
