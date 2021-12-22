"""
2018 Day 1
https://adventofcode.com/2018/day/1
"""

from itertools import cycle
from typing import Optional, Sequence
import aocd  # type: ignore


def frequency_visited_twice(seq: Sequence[int]) -> Optional[int]:
    total = 0
    visited = set()
    for item in cycle(seq):
        total += item
        if total in visited:
            return total
        visited.add(total)
    return None


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2018, day=1)
    sequence = [int(line) for line in data.split("\n")]

    print(f"Part 1: {sum(sequence)}")
    print(f"Part 2: {frequency_visited_twice(sequence)}")


if __name__ == "__main__":
    main()
