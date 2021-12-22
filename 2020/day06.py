"""
2020 Day 6
https://adventofcode.com/2020/day/6
"""

from functools import reduce
from operator import __or__ as union, __and__ as intersection
import aocd  # type: ignore


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2020, day=6)
    groups = [[set(form) for form in group.split("\n")] for group in data.split("\n\n")]

    part1 = sum(len(reduce(union, group)) for group in groups)
    print(f"Part 1: {part1}")

    part2 = sum(len(reduce(intersection, group)) for group in groups)
    print(f"Part 2: {part2}")


if __name__ == "__main__":
    main()
