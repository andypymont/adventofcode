"""
2017 Day 1
https://adventofcode.com/2017/day/1
"""

from typing import Sequence
import aocd  # type: ignore


def read_digits(text: str) -> Sequence[int]:
    return [int(char) for char in text]


def check_sum(digits: Sequence[int], leap: int = 1) -> int:
    return sum(digit for ix, digit in enumerate(digits) if digit == digits[ix - leap])


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2017, day=1)
    digits = read_digits(data)

    print(f"Part 1: {check_sum(digits)}")
    leap = len(digits) // 2
    print(f"Part 2: {check_sum(digits, leap)}")


if __name__ == "__main__":
    main()
