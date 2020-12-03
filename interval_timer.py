import asyncio
import enum

from event import Event

class IntervalTimer:
    def __init__(self):
        # Set up the events that any announcement services can listen to.
        self.started = Event()
        self.tick = Event()
        self.ended = Event()

        self._repetitions = 4
        self._work = 45
        self._rest = 15

        self._task = None

    def running(self):
        return not (self._task is None or self._task.done())

    def print_config(self):
        return f'{self._repetitions} repetitions of {self._work} seconds work and {self._rest} seconds rest'

    def start(self, repetitions: int, work: int, rest: int):
        self._repetitions = repetitions
        self._work = work
        self._rest = rest
        
        self._task = asyncio.create_task(self._run_timer())
        self.started.invoke()
        print('Timer started.')

    def restart(self):
        self._task = asyncio.create_task(self._run_timer())
        self.started.invoke()
        print('Timer started.')

    def stop(self):
        self._task.cancel()
        print('Timer stopped.')

    async def _run_timer(self):
        # Start with a prep phase
        prep = 17
        prep_done = 0
        while prep_done < prep:
            await asyncio.sleep(1)
            prep_done += 1
            self.tick.invoke(phase=TimerPhase.Preparation, done=prep_done, remaining=prep - prep_done)
        
        # Note that the limits are exclusive upper bounds since we count starting from 0.
        repetitions_done = 0
        while repetitions_done < self._repetitions:

            # Work phase.
            work_done = 0
            while work_done < self._work:
                await asyncio.sleep(1)
                work_done += 1
                self.tick.invoke(phase=TimerPhase.Work, done=work_done, remaining=self._work - work_done)
            
            repetitions_done += 1
            # No need to do the rest phase after the last interval.
            if repetitions_done == self._repetitions:
                break

            # Rest phase.
            rest_done = 0
            while rest_done < self._rest:
                await asyncio.sleep(1)
                rest_done += 1
                self.tick.invoke(phase=TimerPhase.Rest, done=rest_done, remaining=self._rest - rest_done)
        
        # Wait to not clash with the last tick event.
        await asyncio.sleep(1)
        self.ended.invoke()
        print('Last interval completed.')


class TimerPhase(enum.Enum):
    Preparation = 1
    Work = 2
    Rest = 3