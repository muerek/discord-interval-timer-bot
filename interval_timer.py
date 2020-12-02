import asyncio
import enum

from event import Event

class IntervalTimer:
    def __init__(self, repetitions: int, work: int, rest: int):
        # Set up the events that any announcement services can listen to.
        self.started = Event()
        self.tick = Event()
        self.ended = Event()

        # Config should not be modified after it is set.
        self._repetitions = repetitions
        self._work = work
        self._rest = rest

    def start(self):
        print('Timer started.')
        self._task = asyncio.create_task(self._run_timer())
        self.started.notify()

    def stop(self):
        print('Timer stopped.')
        self._task.cancel()

    async def _run_timer(self):
        # Note that the limits are exclusive upper bounds since we count starting from 0.
        repetitions_done = 0
        while repetitions_done < self._repetitions:

            # Work phase.
            work_done = 0
            while work_done < self._work:
                await asyncio.sleep(1)
                work_done += 1
                self.tick.notify(phase=TimerPhase.Work, done=work_done, remaining=self._work - work_done)
            
            # Rest phase.
            rest_done = 0
            while rest_done < self._rest:
                await asyncio.sleep(1)
                rest_done += 1
                self.tick.notify(phase=TimerPhase.Rest, done=rest_done, remaining=self._rest - rest_done)
            
            repetitions_done += 1
        
        self.ended.notify()


class TimerPhase(enum.Enum):
    Preparation = 1
    Work = 2
    Rest = 3