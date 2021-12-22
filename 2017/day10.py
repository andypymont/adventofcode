"""
2017 Day 10
https://adventofcode.com/2017/day/10
"""

from functools import reduce
from math import prod
from operator import xor
from typing import Tuple
import aocd  # type: ignore

Lengths = Tuple[int, ...]


def read_lengths(text: str, is_ascii: bool = False) -> Lengths:
    if is_ascii:
        return tuple(ord(char) for char in text)
    return tuple(int(length) for length in text.split(","))


def slice_circle(circle: Lengths, start: int, length: int) -> Lengths:
    return (
        circle[start : start + length]
        + circle[0 : max(start + length - len(circle), 0)]
    )


def reverse_section(circle: Lengths, pos: int, length: int) -> Lengths:
    section = slice_circle(circle, pos, length)
    reversed_section = section[::-1]
    replacements = dict(zip(section, reversed_section))
    return tuple(replacements.get(item, item) for item in circle)


def tie_knots(size: int, lengths: Lengths) -> Lengths:
    circle = tuple(range(size))
    pos = 0
    skip = 0
    for length in lengths:
        circle = reverse_section(circle, pos, length)
        pos = (pos + length + skip) % size
        skip += 1
    return circle


def knot_hash(lengths: Lengths, rounds: int = 64) -> str:
    lengths = (lengths + (17, 31, 73, 47, 23)) * rounds
    sparse_hash = tie_knots(256, lengths)
    dense_hash = [reduce(xor, sparse_hash[grp : grp + 16]) for grp in range(0, 256, 16)]
    return "".join(f"{char:0{2}x}" for char in dense_hash)


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2017, day=10)

    print(f"Part 1: {prod(tie_knots(256, read_lengths(data))[:2])}")
    print(f"Part 2: {knot_hash(read_lengths(data, True))}")


if __name__ == "__main__":
    main()
