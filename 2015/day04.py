"""
2015 Day 4
https://adventofcode.com/2015/day/4
"""

from hashlib import md5
from itertools import count
from typing import Iterator
import aocd  # type: ignore


def adventcoin(secret_key: str, leading_zeroes: int = 5) -> Iterator[int]:
    """
    Advent-coin generator for the given secret key. Returns only valid advent coin (i.e. beginning
    with the expected number of zeroes). Yielded values are the decimals which generated valid
    advent-coin.
    """
    expected_beginning = "0" * leading_zeroes
    for decimal in count(start=1, step=1):
        attempt = secret_key + str(decimal)
        hexdigest = md5(attempt.encode()).hexdigest()
        if hexdigest[:leading_zeroes] == expected_beginning:
            yield decimal


def test_part1():
    """
    Example for Part 1.
    """
    assert next(adventcoin("abcdef")) == 609043


def main():
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2015, day=4)

    print(f"Part 1: {next(adventcoin(data))}")
    print(f"Part 2: {next(adventcoin(data, 6))}")


if __name__ == "__main__":
    main()
