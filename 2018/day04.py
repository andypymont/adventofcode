"""
2018 Day 4
https://adventofcode.com/2018/day/4
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Sequence, Set
import re
import aocd # type: ignore

re_event = re.compile(r'\[([-: \d]+)\] (.+)')
re_guard_change = re.compile(r'Guard #(\d+) begins shift')
re_wakes_up = re.compile(r'wakes up')
re_falls_asleep = re.compile(r'falls asleep')

@dataclass(frozen=True, eq=True, order=True)
class Event():
    when: datetime
    event: str

    @classmethod
    def from_regex_groups(cls, groups: Sequence[str]) -> 'Event':
        return cls(
            datetime.fromisoformat(groups[0]),
            groups[1]
        )

    @classmethod
    def all_from_text(cls, text: str) -> Sequence['Event']:
        return sorted([cls.from_regex_groups(groups) for groups in re_event.findall(text)])

@dataclass(frozen=True)
class Shift():
    guard: int
    asleep: Set[int]

    @classmethod
    def from_events(cls, guard: int, events: Sequence[Event]) -> 'Shift':
        awake = True
        fell_asleep = 0
        asleep_mins = set()
        for event in events:
            if re_falls_asleep.search(event.event):
                fell_asleep = event.when.minute
            if re_wakes_up.search(event.event):
                for minute in range(fell_asleep, event.when.minute):
                    asleep_mins.add(minute)
                fell_asleep = event.when.minute
        if not awake:
            for minute in range(fell_asleep, 60):
                asleep_mins.add(minute)

        return cls(guard, asleep_mins)

    @classmethod
    def all_from_events(cls, events: Sequence[Event]) -> Sequence['Shift']:
        shifts = []
        guard = this_guard_start = -1
        for event_no, event in enumerate(events):
            guard_change = re_guard_change.search(event.event)
            if guard_change:
                if this_guard_start > -1:
                    shifts.append((guard, events[this_guard_start:event_no]))
                this_guard_start = event_no
                guard = int(guard_change.groups()[0])
        return [cls.from_events(*shift) for shift in shifts]

@dataclass(frozen=True)
class Guard():
    guard: int
    asleep: Dict[int, int]

    @property
    def total_minutes_asleep(self) -> int:
        return sum(times for times in self.asleep.values())

    @property
    def minute_most_often_asleep(self) -> int:
        time_asleep = lambda x: self.asleep.get(x, 0)
        return next(m for m in sorted(self.asleep, key=time_asleep, reverse=True))

    @property
    def most_times_asleep_on_same_minute(self) -> int:
        return max(self.asleep.values())

    @classmethod
    def all_from_shifts(cls, shifts: Sequence[Shift]) -> Sequence['Guard']:
        guards = {}
        for shift in shifts:
            if shift.guard not in guards:
                guards[shift.guard] = dict((minute, 0) for minute in range(60))
            for minute in shift.asleep:
                guards[shift.guard][minute] += 1

        return [cls(guard, asleep) for guard, asleep in guards.items()]

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2018, day=4)

    events = Event.all_from_text(data)
    shifts = Shift.all_from_events(events)
    guards = Guard.all_from_shifts(shifts)

    guard = next(
        g for g in sorted(guards, key=lambda g: g.total_minutes_asleep, reverse=True)
    )
    print(f'Part 1: {guard.guard * guard.minute_most_often_asleep}')

    guard = next(
        g for g in sorted(guards, key=lambda g: g.most_times_asleep_on_same_minute, reverse=True)
    )
    print(f'Part 2: {guard.guard * guard.minute_most_often_asleep}')

if __name__ == '__main__':
    main()
