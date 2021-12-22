"""
2016 Day 16
https://adventofcode.com/2016/day/16
"""

import aocd  # type: ignore
import numpy as np


def dragon(original: np.ndarray) -> np.ndarray:
    """
    Run a dragon curve transformation on a given input array.
    """
    return np.concatenate((original, [0], np.flip(1 - original)))


def fill_disk(initial: str, size: int) -> np.ndarray:
    """
    Repeatedly transform the data with the dragon curve function until a disk of the given size is
    filled.
    """
    disk = np.array([int(digit) for digit in initial], dtype=int)
    while len(disk) < size:
        disk = dragon(disk)
    return disk[:size]


def checksum(disk: np.ndarray) -> np.ndarray:
    """
    Calculate the checksum array from the given base array.
    """
    check = np.array(
        [1 if pair[0] == pair[1] else 0 for pair in np.split(disk, len(disk) // 2)]
    )
    return check if len(check) % 2 == 1 else checksum(check)


def binary_checksum_str(disk: np.ndarray) -> str:
    """
    Calculate the checksum array for the given base array and convert to a string.
    """
    return "".join(str(digit) for digit in checksum(disk))


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2016, day=16)

    print(f"Part 1: {binary_checksum_str(fill_disk(data, 272))}")
    print(f"Part 2: {binary_checksum_str(fill_disk(data, 35_651_584))}")


if __name__ == "__main__":
    main()
