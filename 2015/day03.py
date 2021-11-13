"""
2015 Day 3
https://adventofcode.com/2015/day/3
"""

from dataclasses import dataclass
from typing import Dict, Set
import aocd # type: ignore


@dataclass(frozen=True)
class Point:
    """
    Two-dimensional point with an x and y coordinate.
    """
    x_coord: int
    y_coord: int

    def __add__(self, other: 'Point') -> 'Point':
        return Point(
            self.x_coord + other.x_coord,
            self.y_coord + other.y_coord
        )

COMPASS: Dict[str, Point] = {
    '>': Point(1, 0),
    'v': Point(0, 1),
    '<': Point(-1, 0),
    '^': Point(0, -1),
}

def houses_visited(directions: str) -> Set[Point]:
    """
    Return the set of distinct houses visited by Santa, given he starts at position 0, 0 and
    follows the given set of directions.
    """
    location = Point(0, 0)
    visited = {location}

    for direction in directions:
        location += COMPASS.get(direction, Point(0, 0))
        visited.add(location)

    return visited

def test_part1():
    """
    Examples for Part 1.
    """
    assert len(houses_visited('>')) == 2
    assert len(houses_visited('^>v<')) == 4
    assert len(houses_visited('^v^v^v^v^v')) == 2

def houses_visited_by_two_santas(directions: str) -> Set[Point]:
    """
    Return the set of distinct houses visited by Santa and Robo-Santa, with single steps in the
    given route alternating which Santa they are handed to.
    """
    santa = directions[::2]
    robosanta = directions[1::2]
    return houses_visited(santa).union(houses_visited(robosanta))

def test_part2():
    """
    Examples for Part 2.
    """
    assert len(houses_visited_by_two_santas('^v')) == 3
    assert len(houses_visited_by_two_santas('^>v<')) == 3
    assert len(houses_visited_by_two_santas('^v^v^v^v^v')) == 11

def main():
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2015, day=3)

    print(f'Part 1: {len(houses_visited(data))}')
    print(f'Part 2: {len(houses_visited_by_two_santas(data))}')

if __name__ == '__main__':
    main()
