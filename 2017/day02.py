"""
2017 Day 2
https://adventofcode.com/2017/day/2
"""

from itertools import combinations
from typing import Sequence
import aocd  # type: ignore

Row = Sequence[int]
Sheet = Sequence[Row]


def read_sheet(text: str) -> Sheet:
    return [[int(val) for val in line.split("\t")] for line in text.split("\n")]


def check_sum(sheet: Sheet) -> int:
    return sum(max(row) - min(row) for row in sheet)


def check_row(row: Row) -> int:
    """
    Calculate the part 2 checksum for a single row.
    """
    for (first, second) in combinations(row, 2):
        first, second = (second, first) if (first > second) else (first, second)
        if second % first == 0:
            return second // first
    return 0


def check_sum2(sheet: Sheet) -> int:
    return sum(check_row(row) for row in sheet)


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2017, day=2)
    sheet = read_sheet(data)

    print(f"Part 1: {check_sum(sheet)}")
    print(f"Part 2: {check_sum2(sheet)}")


if __name__ == "__main__":
    main()
