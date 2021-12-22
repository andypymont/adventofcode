"""
2020 Day 1
https://adventofcode.com/2020/day/1
"""

from itertools import combinations
from math import prod
from typing import Iterable
import aocd  # type: ignore


def find_2020(numbers: Iterable[int], howmany: int = 2) -> int:
    for combo in combinations(numbers, howmany):
        if sum(combo) == 2020:
            return prod(combo)
    return -1


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2020, day=1)
    numbers = [int(line) for line in data.split("\n")]

    print(f"Part 1: {find_2020(numbers)}")
    print(f"Part 2: {find_2020(numbers, 3)}")


if __name__ == "__main__":
    main()
