"""
2021 Day 2
https://adventofcode.com/2021/day/2
"""

from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Tuple
import aocd # type: ignore

class Direction(Enum):
    DOWN = 'down'
    UP = 'up'
    FORWARD = 'forward'

@dataclass(frozen=True, order=True)
class Move:
    direction: Direction
    distance: int

    @classmethod
    def from_description(cls, description: str) -> 'Move':
        direction, distance, *_ = description.split(' ')
        return cls(Direction(direction), int(distance))

def follow_moves(moves: Iterable[Move]) -> Tuple[int, int]:
    depth = horizontal = 0
    for move in moves:
        if move.direction == Direction.UP:
            depth -= move.distance
        elif move.direction == Direction.DOWN:
            depth += move.distance
        elif move.direction == Direction.FORWARD:
            horizontal += move.distance
    return (depth, horizontal)

def follow_moves2(moves: Iterable[Move]) -> Tuple[int, int]:
    depth = horizontal = aim = 0
    for move in moves:
        if move.direction == Direction.DOWN:
            aim += move.distance
        elif move.direction == Direction.UP:
            aim -= move.distance
        elif move.direction == Direction.FORWARD:
            horizontal += move.distance
            depth += (aim * move.distance)
    return (depth, horizontal)

def test_part1() -> None:
    """
    Examples for Part 1.
    """
    assert Move.from_description('forward 5') == Move(Direction.FORWARD, 5)
    assert Move.from_description('down 5') == Move(Direction.DOWN, 5)
    assert Move.from_description('forward 8') == Move(Direction.FORWARD, 8)
    assert Move.from_description('up 3') == Move(Direction.UP, 3)
    assert Move.from_description('down 8') == Move(Direction.DOWN, 8)
    assert Move.from_description('forward 2') == Move(Direction.FORWARD, 2)

    moves = (
        Move(Direction.FORWARD, 5),
        Move(Direction.DOWN, 5),
        Move(Direction.FORWARD, 8),
        Move(Direction.UP, 3),
        Move(Direction.DOWN, 8),
        Move(Direction.FORWARD, 2)
    )

    assert follow_moves(moves) == (10, 15)

def test_part2() -> None:
    """
    Examples for Part 2.
    """
    moves = (
        Move(Direction.FORWARD, 5),
        Move(Direction.DOWN, 5),
        Move(Direction.FORWARD, 8),
        Move(Direction.UP, 3),
        Move(Direction.DOWN, 8),
        Move(Direction.FORWARD, 2)
    )

    assert follow_moves2(moves) == (60, 15)

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2021, day=2)
    moves = [Move.from_description(line) for line in data.split('\n')]

    p1_depth, p1_dist = follow_moves(moves)
    print(f'Part 1: {p1_depth * p1_dist}')

    p2_depth, p2_dist = follow_moves2(moves)
    print(f'Part 2: {p2_depth * p2_dist}')

if __name__ == '__main__':
    main()
