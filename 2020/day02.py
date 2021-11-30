"""
2020 Day 2
https://adventofcode.com/2020/day/2
"""

import re
from typing import Callable
import aocd # type: ignore

def matches_sled_policy(lbound: int, ubound: int, letter: str, word: str) -> bool:
    return int(lbound) <= sum(1 for char in word if char == letter) <= int(ubound)

def valid_passwords(
    text: str,
    checker: Callable[[int, int, str, str], bool] = matches_sled_policy
) -> int:
    return sum(
        1 for example in re.findall(r'(\d+)-(\d+) (\w): (\w+)', text)
        if checker(*example)
    )

def matches_toboggan_policy(
    index1: int,
    index2: int,
    letter: str,
    word: str
) -> bool:
    first = 1 if word[int(index1)-1] == letter else 0
    second = 1 if word[int(index2)-1] == letter else 0
    return first + second == 1

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2020, day=2)

    print(f'Part 1: {valid_passwords(data)}')
    print(f'Part 2: {valid_passwords(data, matches_toboggan_policy)}')

if __name__ == '__main__':
    main()
