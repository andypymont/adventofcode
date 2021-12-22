"""
2017 Day 3
https://adventofcode.com/2017/day/3
"""

from collections import OrderedDict
from dataclasses import dataclass
from typing import Iterator
import aocd  # type: ignore


@dataclass(frozen=True)
class Point:
    y_coord: int
    x_coord: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.y_coord + other.y_coord, self.x_coord + other.x_coord)

    @property
    def taxicab(self) -> int:
        return abs(self.y_coord) + abs(self.x_coord)

    @property
    def neighbours(self) -> Iterator["Point"]:
        for delta_x, delta_y in (
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ):
            yield Point(self.y_coord + delta_y, self.x_coord + delta_x)


UP = Point(-1, 0)
DOWN = Point(1, 0)
LEFT = Point(0, -1)
RIGHT = Point(0, 1)
TURN_LEFT = {
    UP: LEFT,
    LEFT: DOWN,
    DOWN: RIGHT,
    RIGHT: UP,
}


class Memory:
    def __init__(self) -> None:
        self.memory = OrderedDict()
        self.memory[Point(0, 0)] = 1
        self.pos = Point(0, 1)
        self.dir = RIGHT

    def populate_next(self) -> None:
        self.memory[self.pos] = sum(
            self.memory.get(neighbour, 0) for neighbour in self.pos.neighbours
        )
        if self.pos + TURN_LEFT[self.dir] not in self.memory:
            self.dir = TURN_LEFT[self.dir]
        self.pos += self.dir

    def coords_from_index(self, index: int) -> Point:
        while len(self.memory) < index:
            self.populate_next()
        return list(self.memory.keys())[index - 1]

    def first_larger_value(self, target: int) -> int:
        return next(value for value in self.memory.values() if value > target)


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2017, day=3)
    target = int(data)
    mem = Memory()

    print(f"Part 1: {mem.coords_from_index(target).taxicab}")
    print(f"Part 2: {mem.first_larger_value(target)}")


if __name__ == "__main__":
    main()
