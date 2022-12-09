"""
2022 Day 9
https://adventofcode.com/2022/day/9
"""

from dataclasses import dataclass
from enum import Enum
from typing import Iterator
import aocd  # type: ignore


@dataclass(frozen=True, order=True)
class Point:
    """
    A 2-dimensional point, consisting of y and x coordinates.
    """

    y_coord: int
    x_coord: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.y_coord + other.y_coord, self.x_coord + other.x_coord)

    def toward(self, other: "Point") -> "Point":
        """
        Return a point representing a one-step vector y, x to move from this point in the direction
        of the given second point.
        """
        return Point(
            1
            if other.y_coord > self.y_coord
            else -1
            if other.y_coord < self.y_coord
            else 0,
            1
            if other.x_coord > self.x_coord
            else -1
            if other.x_coord < self.x_coord
            else 0,
        )


class Direction(Enum):
    """
    A direction: up, down, left, or right in 2-dimensional space.
    """

    UP = Point(-1, 0)
    DOWN = Point(1, 0)
    LEFT = Point(0, -1)
    RIGHT = Point(0, 1)

    @classmethod
    def from_char(cls, char: str) -> "Direction":
        """
        Convert a single-character string into the corresponding direction.
        """
        if char == "U":
            return cls.UP
        if char == "D":
            return cls.DOWN
        if char == "L":
            return cls.LEFT
        if char == "R":
            return cls.RIGHT
        raise ValueError


def read_move(line: str) -> tuple[Direction, int]:
    """
    Read a move from a single line of the puzzle input, returning a tuple of the Direction and an
    int representing the number of steps.
    """
    parts = line.split(" ")
    return Direction.from_char(parts[0]), int(parts[1])


def read_moves(text: str) -> tuple[tuple[Direction, int], ...]:
    """
    Read all the moves from the puzzle input, returning them as a tuple of tuples, with the inner
    tuples being in the format (direction: Direction, steps: int).
    """
    return tuple(read_move(line) for line in text.split("\n"))


@dataclass(frozen=True, order=True)
class Rope:
    """
    A rope, consisting of the position of its head and tail (which may overlap) in 2d space.
    """
    head: Point
    tail: Point

    def step(self, direction: Direction) -> "Rope":
        """
        Return the state reached by moving the head of the rope one step in the given direction,
        with the tail following as needed.
        """
        head = self.head + direction.value
        tail = self.tail + self.tail.toward(head)
        return Rope(head, self.tail if tail == head else tail)

    def move(self, direction: Direction, steps: int) -> Iterator["Rope"]:
        """
        Yield each state of the rope reached in moving the head of the rope the given number of
        steps in the given direction.
        """
        rope = self
        for _ in range(steps):
            rope = rope.step(direction)
            yield rope


def positions_visited_by_tail(moves: tuple[tuple[Direction, int], ...]) -> int:
    """
    Simulate the movement of the rope from an initial position with head and tail both at the same
    point, and return the number of distinct locations visited by the tail.
    """
    origin = Point(0, 0)
    rope = Rope(origin, origin)
    visited = {origin}

    for direction, steps in moves:
        for state in rope.move(direction, steps):
            rope = state
            visited.add(rope.tail)

    return len(visited)


def test_part1() -> None:
    """
    Examples for Part 1.
    """
    assert Point(5, 0).toward(Point(2, 0)) == Point(-1, 0)
    assert Point(2, 2).toward(Point(2, 4)) == Point(0, 1)
    assert Point(4, 7).toward(Point(8, 11)) == Point(1, 1)

    assert Rope(Point(0, 0), Point(0, 0)).step(Direction.RIGHT) == Rope(
        Point(0, 1), Point(0, 0)
    )
    assert Rope(Point(0, 1), Point(0, 0)).step(Direction.RIGHT) == Rope(
        Point(0, 2), Point(0, 1)
    )

    assert set(Rope(Point(0, 0), Point(0, 0)).move(Direction.RIGHT, 4)) == {
        Rope(Point(0, 1), Point(0, 0)),
        Rope(Point(0, 2), Point(0, 1)),
        Rope(Point(0, 3), Point(0, 2)),
        Rope(Point(0, 4), Point(0, 3)),
    }

    assert Rope(Point(0, 4), Point(0, 3)).step(Direction.UP) == Rope(
        Point(-1, 4), Point(0, 3)
    )
    assert set(Rope(Point(0, 4), Point(0, 3)).move(Direction.UP, 4)) == {
        Rope(Point(-1, 4), Point(0, 3)),
        Rope(Point(-2, 4), Point(-1, 4)),
        Rope(Point(-3, 4), Point(-2, 4)),
        Rope(Point(-4, 4), Point(-3, 4)),
    }

    example = (
        (Direction.RIGHT, 4),
        (Direction.UP, 4),
        (Direction.LEFT, 3),
        (Direction.DOWN, 1),
        (Direction.RIGHT, 4),
        (Direction.DOWN, 1),
        (Direction.LEFT, 5),
        (Direction.RIGHT, 2),
    )
    assert (
        read_moves(
            "\n".join(
                (
                    "R 4",
                    "U 4",
                    "L 3",
                    "D 1",
                    "R 4",
                    "D 1",
                    "L 5",
                    "R 2",
                )
            )
        )
        == example
    )

    assert positions_visited_by_tail(example) == 13


# def test_part2() -> None:
#     """
#     Examples for Part 2.
#     """
#     assert False


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2022, day=9)
    moves = read_moves(data)

    part_one = positions_visited_by_tail(moves)
    print(f"Part 1: {part_one}")
    # print(f'Part 2: {part_two}')


if __name__ == "__main__":
    main()
