"""
2020 Day 9
https://adventofcode.com/2020/day/9
"""

from itertools import combinations
from typing import Sequence, Set, Tuple
import aocd  # type: ignore


def read_sequence(text: str) -> Tuple[int, ...]:
    return tuple(map(int, text.split("\n")))


def totals(items: Sequence[int]) -> Set[int]:
    return {a + b for a, b in combinations(items, 2)}


def first_invalid_number(sequence: Sequence[int], preamble: int = 25) -> int:
    for index in range(preamble, len(sequence)):
        if sequence[index] not in totals(sequence[index - preamble : index]):
            return sequence[index]
    raise ValueError


def find_series_that_totals(sequence: Sequence[int], target: int) -> int:
    for finish in range(len(sequence)):
        for start in range(finish):
            subsequence = sequence[start:finish]
            if sum(subsequence) == target:
                return min(subsequence) + max(subsequence)
    raise ValueError


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2020, day=9)
    seq = read_sequence(data)

    first = first_invalid_number(seq)
    print(f"Part 1: {first}")
    print(f"Part 2: {find_series_that_totals(seq, first)}")


if __name__ == "__main__":
    main()
