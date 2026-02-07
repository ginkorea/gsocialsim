import datetime
import random
from dataclasses import dataclass

@dataclass
class SimClock:
    t: int = 0  # Total simulation ticks
    day: int = 0  # Current simulation day
    tick_of_day: int = 0  # Current tick within the day
    ticks_per_day: int = 1440 # 1440 minutes in a day, assuming 1 tick = 1 minute

    def advance(self, num_ticks: int = 1):
        self.t += num_ticks
        self.tick_of_day += num_ticks
        while self.tick_of_day >= self.ticks_per_day:
            self.tick_of_day -= self.ticks_per_day
            self.day += 1

    def get_datetime(self, start_date: datetime.datetime) -> datetime.datetime:
        """
        Returns the current simulation datetime based on a start_date.
        Assumes each tick is one minute.
        """
        return start_date + datetime.timedelta(minutes=self.t)

