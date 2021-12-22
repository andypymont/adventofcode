"""
2015 Day 17
https://adventofcode.com/2015/day/17
"""

from typing import Iterable, Sequence
import numpy as np
import aocd  # type: ignore


def read_containers(text: str) -> Sequence[int]:
    """
    Read the puzzle input into a list of integers representing the container sizes.
    """
    return [int(line) for line in text.split("\n")]


def valid_combos(
    containers: Sequence[int], target: int = 150
) -> Iterable[Sequence[int]]:
    """
    Calculate all valid container combinations which add up to the total target quantity.
    """
    format_str = "{:0>" + str(len(containers)) + "}"

    def binary(number):
        """
        Convert a number into the appropriate-length binary representation.
        """
        return format_str.format(np.base_repr(number, 2))

    for combo in range(1, 2 ** len(containers)):
        bits = binary(combo)
        selected = [
            container for c, container in enumerate(containers) if bits[c] == "1"
        ]
        if sum(selected) == target:
            yield selected


def main():
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2015, day=17)
    containers = read_containers(data)
    combos = tuple(valid_combos(containers))

    print(f"Part 1: {len(combos)}")

    min_containers = min(len(c) for c in combos)
    possibilities = [combo for combo in combos if len(combo) == min_containers]

    print(f"Part 2: {len(possibilities)}")


if __name__ == "__main__":
    main()
