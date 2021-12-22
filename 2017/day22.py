"""
2017 Day 22
https://adventofcode.com/2017/day/22
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Set, Tuple
import aocd  # type: ignore


@dataclass(frozen=True)
class Point:
    y_coord: int
    x_coord: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.y_coord + other.y_coord, self.x_coord + other.x_coord)


UP = Point(-1, 0)
RIGHT = Point(0, 1)
DOWN = Point(1, 0)
LEFT = Point(0, -1)
TURN_LEFT = {UP: LEFT, LEFT: DOWN, DOWN: RIGHT, RIGHT: UP}
TURN_RIGHT = {UP: RIGHT, LEFT: UP, DOWN: LEFT, RIGHT: DOWN}


def read_input(text: str) -> Tuple[Set[Point], Point]:
    lines = text.split("\n")

    center = len(lines) // 2
    position = Point(center, center)

    infected = set()
    for y_coord, line in enumerate(lines):
        for x_coord, char in enumerate(line):
            if char == "#":
                infected.add(Point(y_coord, x_coord))

    return infected, position


def carrier_activity(initial_infected: Set[Point], position: Point, bursts: int) -> int:
    infected = set(initial_infected)
    direction = UP
    count = 0

    for _ in range(bursts):
        if position in infected:
            direction = TURN_RIGHT[direction]
            infected.remove(position)
        else:
            direction = TURN_LEFT[direction]
            infected.add(position)
            count += 1

        position += direction

    return count


class Status(Enum):
    CLEAN = 0
    WEAKENED = 1
    INFECTED = 2
    FLAGGED = 3


REVERSE = {
    UP: DOWN,
    LEFT: RIGHT,
    DOWN: UP,
    RIGHT: LEFT,
}


def read_input2(text: str) -> Tuple[Dict[Point, Status], Point]:
    lines = text.split("\n")

    center = len(lines) // 2
    position = Point(center, center)

    grid = {}
    for y_coord, line in enumerate(lines):
        for x_coord, char in enumerate(line):
            if char == "#":
                grid[Point(y_coord, x_coord)] = Status.INFECTED
            else:
                grid[Point(y_coord, x_coord)] = Status.CLEAN

    return grid, position


def carrier_activity2(
    initial_grid: Dict[Point, Status], position: Point, bursts: int
) -> int:
    grid = dict(initial_grid)
    direction = UP
    count = 0

    for _ in range(bursts):
        state = grid.get(position, Status.CLEAN)
        if state == Status.CLEAN:
            direction = TURN_LEFT[direction]
            grid[position] = Status.WEAKENED
        elif state == Status.WEAKENED:
            grid[position] = Status.INFECTED
            count += 1
        elif state == Status.INFECTED:
            direction = TURN_RIGHT[direction]
            grid[position] = Status.FLAGGED
        elif state == Status.FLAGGED:
            direction = REVERSE[direction]
            grid[position] = Status.CLEAN

        position += direction

    return count


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2017, day=22)

    infected, position = read_input(data)
    print(f"Part 1: {carrier_activity(infected, position, 10_000)}")

    grid, position = read_input2(data)
    print(f"Part 2: {carrier_activity2(grid, position, 10_000_000)}")


if __name__ == "__main__":
    main()
