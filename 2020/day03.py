"""
2020 Day 3
https://adventofcode.com/2020/day/3
"""

from dataclasses import dataclass
from math import prod
from typing import Iterator, Sequence
import aocd  # type: ignore


@dataclass(frozen=True)
class Vector:
    x: int
    y: int

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)

    def repeat(self) -> Iterator[Vector]:
        current = self
        while True:
            yield current
            current += self


def read_slope(text: str) -> Sequence[Sequence[int]]:
    return [[1 if char == "#" else 0 for char in line] for line in text.split("\n")]


def trees_on_trajectory(slope: Sequence[Sequence[int]], vector: Vector) -> int:
    trees = 0
    trajectory = vector.repeat()
    columns = len(slope[0])
    while True:
        point = next(trajectory)
        if point.y >= len(slope):
            return trees
        trees += 1 if slope[point.y][point.x % columns] else 0


TRAJECTORIES = (
    Vector(1, 1),
    Vector(3, 1),
    Vector(5, 1),
    Vector(7, 1),
    Vector(1, 2),
)


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2020, day=3)

    slope = read_slope(data)
    trees_encountered = {
        trajectory: trees_on_trajectory(slope, trajectory)
        for trajectory in TRAJECTORIES
    }

    print(f"Part 1: {trees_encountered[Vector(3, 1)]}")
    print(f"Part 2: {prod(trees_encountered.values())}")


if __name__ == "__main__":
    main()
