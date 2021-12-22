"""
2020 Day 13
https://adventofcode.com/2020/day/13
"""

import re
from typing import Sequence, Tuple
import aocd  # type: ignore

RE_BUSES = re.compile(r"(\d+)")


def read_input(text: str) -> Sequence[int]:
    return [int(x) for x in RE_BUSES.findall(text)]


def find_first_departure(minute: int, buses: Sequence[int]) -> Tuple[int, int]:
    while True:
        for bus in buses:
            if minute % bus == 0:
                return minute, bus
        minute += 1


RE_ALL_BUSES = re.compile(r"([\dx]+)")


def read_schedule(text: str) -> Sequence[Tuple[int, int]]:
    return tuple(
        (int(bus), match - 1)
        for match, bus in enumerate(RE_ALL_BUSES.findall(text))
        if bus.isdigit()
    )[1:]


def first_minute_matching_schedule(schedule: Sequence[Tuple[int, int]]) -> int:
    matching = 1
    increment = schedule[0][0]
    total = 0
    while matching < len(schedule):
        value, remainder = schedule[matching]
        departure = (value - remainder) % value
        while (total % value) != departure:
            total += increment
        increment *= value
        matching += 1
    return total


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2020, day=13)

    time, *buses = read_input(data)

    p1_time, p1_bus = find_first_departure(time, buses)
    print(
        f"Part 1: wait {p1_time-time} minutes for bus {p1_bus}: {(p1_time-time)*p1_bus}"
    )

    schedule = read_schedule(data)
    print(f"Part 2: {first_minute_matching_schedule(schedule)}")


if __name__ == "__main__":
    main()
