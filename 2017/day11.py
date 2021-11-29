"""
2017 Day 11
https://adventofcode.com/2017/day/11
"""

from dataclasses import dataclass
from typing import Dict, Iterator, Sequence
import aocd # type: ignore

@dataclass(frozen=True)
class Point:
    x_coord: int
    y_coord: int

    @property
    def z_coord(self) -> int:
        return 0 - self.y_coord - self.x_coord

    @property
    def distance(self) -> int:
        return (abs(self.x_coord) + abs(self.y_coord) + abs(self.z_coord)) // 2

    def __add__(self, other: 'Point') -> 'Point':
        return Point(self.x_coord + other.x_coord, self.y_coord + other.y_coord)

DIRECTIONS: Dict[str, Point] = {
    'n': Point(x_coord=0, y_coord=1),
    'ne': Point(x_coord=1, y_coord=0),
    'se': Point(x_coord=1, y_coord=-1),
    's': Point(x_coord=0, y_coord=-1),
    'sw': Point(x_coord=-1, y_coord=0),
    'nw': Point(x_coord=-1, y_coord=1),
}

def distances_on_journey(steps: Sequence[str]) -> Iterator[int]:
    pos = Point(0, 0)
    for step in steps:
        pos += DIRECTIONS[step]
        yield pos.distance

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2017, day=11)

    steps = data.split(',')
    distances = list(distances_on_journey(steps))

    print(f'Part 1: {distances[-1]}')
    print(f'Part 2: {max(distances)}')

if __name__ == '__main__':
    main()
