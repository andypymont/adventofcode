"""
2022 Day 4
https://adventofcode.com/2022/day/4
"""

from collections import Counter
from enum import Enum
from typing import Tuple
import re
import aocd  # type: ignore

re_pair = re.compile(r"(\d+)-(\d+),(\d+)-(\d+)")


def read_pairs(text: str) -> Tuple[tuple[int, int, int, int], ...]:
    """
    Read the pairs from the puzzle input and return them as a tuple of four ints.
    """
    return tuple(
        (int(match[0]), int(match[1]), int(match[2]), int(match[3]))
        for match in re_pair.findall(text)
    )


class Overlap(Enum):
    """
    Enumeration representing one of the possible overlap states in the pair: either no overlap,
    a partial overlap, or one range fully containing the other.
    """

    NONE = 0
    PARTIAL = 1
    FULL = 2


def overlap_type(pair: Tuple[int, int, int, int]) -> Overlap:
    """
    Return the type of Overlap enum present in the given pair.
    """
    if (pair[0] >= pair[2] and pair[1] <= pair[3]) or (
        pair[2] >= pair[0] and pair[3] <= pair[1]
    ):
        return Overlap.FULL
    if pair[0] >= pair[2] and pair[0] <= pair[3]:
        return Overlap.PARTIAL
    if pair[2] >= pair[0] and pair[2] <= pair[1]:
        return Overlap.PARTIAL

    return Overlap.NONE


def test_parts_1_and_2() -> None:
    """
    Examples for Part 1.
    """
    example_input = "\n".join(
        (
            "2-4,6-8",
            "2-3,4-5",
            "5-7,7-9",
            "2-8,3-7",
            "6-6,4-6",
            "2-6,4-8",
            "25-31,57-102",
        )
    )
    examples = (
        (2, 4, 6, 8),
        (2, 3, 4, 5),
        (5, 7, 7, 9),
        (2, 8, 3, 7),
        (6, 6, 4, 6),
        (2, 6, 4, 8),
        (25, 31, 57, 102),
    )
    assert read_pairs(example_input) == examples
    assert overlap_type(examples[0]) == Overlap.NONE
    assert overlap_type(examples[1]) == Overlap.NONE
    assert overlap_type(examples[2]) == Overlap.PARTIAL
    assert overlap_type(examples[3]) == Overlap.FULL
    assert overlap_type(examples[4]) == Overlap.FULL
    assert overlap_type(examples[5]) == Overlap.PARTIAL
    assert overlap_type(examples[6]) == Overlap.NONE


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2022, day=4)
    overlaps = Counter(overlap_type(pair) for pair in read_pairs(data))

    part_one = overlaps.get(Overlap.FULL, 0)
    print(f"Part 1: {part_one}")
    part_two = overlaps.get(Overlap.PARTIAL, 0) + part_one
    print(f"Part 2: {part_two}")


if __name__ == "__main__":
    main()
