"""
2020 Day 25
https://adventofcode.com/2020/day/25
"""

from itertools import count
import aocd  # type: ignore


def encrypt(subject: int, loopsize: int) -> int:
    return pow(subject, loopsize, 20201227)


def calculate_loop_size(key: int) -> int:
    for loop_size in count(1):
        if encrypt(7, loop_size) == key:
            return loop_size
    raise ValueError


def calculate_encryption_key(door_key: int, card_key: int) -> int:
    door_loop_size = calculate_loop_size(door_key)
    return encrypt(card_key, door_loop_size)


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2020, day=25)

    keys = tuple(int(key) for key in data.split("\n"))
    print(f"Part 1: {calculate_encryption_key(*keys)}")


if __name__ == "__main__":
    main()
