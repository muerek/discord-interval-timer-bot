import asyncio

from interval_timer import IntervalTimer


class VoiceAnnouncer():
    def __init__(self, context, timer: IntervalTimer):
        self._context = context
        # Attach to the timer events.
        timer.started += self.on_timer_started
        timer.tick += self.on_timer_tick
        timer.ended += self.on_timer_ended

    def on_timer_tick(self, phase, done, remaining):
        print(f'Phase {phase} with {done} seconds done and {remaining} seconds remaining.')
        # In C#, I would have an async void event handler here. Any Task would return hot and started.
        # This is my attempt to do the same here. Python does not return hot tasks, but we need to explicitly start them.
        asyncio.create_task(self._context.send(f'Phase {phase} with {done} seconds done and {remaining} seconds remaining.'))

    def on_timer_started(self):
        print('Timer started.')

    def on_timer_ended(self):
        print('All done.')