"""
2017 Day 14
https://adventofcode.com/2017/day/14
"""

from dataclasses import dataclass
from functools import reduce
from operator import xor
from typing import Optional, Sequence, Set, Tuple
import aocd # type: ignore

Lengths = Tuple[int, ...]

def read_lengths(text: str) -> Lengths:
    return tuple(ord(char) for char in text)

def slice_circle(circle: Lengths, start: int, length: int) -> Lengths:
    return circle[start:start+length] + circle[0:max(start+length-len(circle), 0)]

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

def knot_hash(text: str, rounds: int = 64) -> str:
    lengths = (read_lengths(text) + (17, 31, 73, 47, 23)) * rounds
    sparse_hash = tie_knots(256, lengths)
    dense_hash = [reduce(xor, sparse_hash[grp:grp+16]) for grp in range(0, 256, 16)]
    return ''.join(f'{char:0{2}x}' for char in dense_hash)

@dataclass(frozen=True)
class Point:
    y_coord: int
    x_coord: int

    def __add__(self, other: 'Point') -> 'Point':
        return Point(self.y_coord + other.y_coord, self.x_coord + other.x_coord)

def dense_hash_to_digits(dense_hash: Sequence[str]) -> Sequence[int]:
    digits = []
    for char in dense_hash:
        digits.append(int(char, 16))
    return digits

def row(key: str, row_number: int) -> str:
    digits = dense_hash_to_digits(knot_hash(f'{key}-{row_number}'))
    return ''.join(f'{digit:04b}' for digit in digits)

def occupied_squares(key: str) -> Set[Point]:
    occupied = set()
    for y_coord in range(128):
        for x_coord, char in enumerate(row(key, y_coord)):
            if char == '1':
                occupied.add(Point(y_coord, x_coord))
    return occupied

ADJACENT = [
    Point(0, -1),
    Point(0, 1),
    Point(1, 0),
    Point(-1, 0),
]

def region(occupied: Set[Point], origin: Point, visited: Optional[Set[Point]] = None) -> Set[Point]:
    visited = visited if visited else set()
    visited.add(origin)
    for direction in ADJACENT:
        neighbour = origin + direction
        if (neighbour in occupied) and (neighbour not in visited):
            visited = visited.union(region(occupied, neighbour, visited))
    return visited

def all_regions(occupied: Set[Point]) -> Set[Tuple[Tuple[int, int], ...]]:
    regions = set()
    mapped: Set[Point] = set()
    while len(mapped) < len(occupied):
        candidate = next(occ for occ in occupied if occ not in mapped)
        candidate_region = region(occupied, candidate)
        mapped = mapped.union(candidate_region)
        regions.add(tuple((pt.y_coord, pt.x_coord) for pt in candidate_region))
    return regions

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2017, day=14)

    occupied = occupied_squares(data)
    print(f'Part 1: {len(occupied)}')

    regions = all_regions(occupied)
    print(f'Part 2: {len(regions)}')

if __name__ == '__main__':
    main()
