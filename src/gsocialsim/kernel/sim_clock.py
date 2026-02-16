import datetime
from dataclasses import dataclass


@dataclass
class SimClock:
    """
    Contract clock.

    - 1 tick = 900 seconds (15 minutes)
    - 96 ticks per day
    """
    t: int = 0               # Total simulation ticks
    day: int = 0             # Current simulation day
    tick_of_day: int = 0     # Current tick within the day

    seconds_per_tick: int = 900
    ticks_per_day: int = 96  # 24h * 60min / 15min = 96

    def advance(self, num_ticks: int = 1) -> None:
        if num_ticks <= 0:
            return

        self.t += num_ticks
        self.tick_of_day += num_ticks
        while self.tick_of_day >= self.ticks_per_day:
            self.tick_of_day -= self.ticks_per_day
            self.day += 1

    def get_datetime(self, start_date: datetime.datetime) -> datetime.datetime:
        """
        Returns the current simulation datetime based on start_date.
        Assumes each tick is 15 minutes (900 seconds).
        """
        return start_date + datetime.timedelta(seconds=self.t * self.seconds_per_tick)

    def get_tod_minutes(self) -> int:
        """Minutes into the current day."""
        return self.tick_of_day * (self.seconds_per_tick // 60)
