"""
2020 Day 12
https://adventofcode.com/2020/day/12
"""

from dataclasses import dataclass
from typing import List, Tuple
import re
import aocd # type: ignore

@dataclass(frozen=True, order=True)
class Point:
    y_coord: int
    x_coord: int

    def __add__(self, other: 'Point') -> 'Point':
        return Point(self.y_coord+other.y_coord, self.x_coord+other.x_coord)

    def __mul__(self, other: int) -> 'Point':
        return Point(self.y_coord*other, self.x_coord*other)

    @property
    def manhattan_distance(self) -> int:
        return abs(self.y_coord) + abs(self.x_coord)

NORTH = Point(y_coord=1, x_coord=0)
EAST = Point(y_coord=0, x_coord=1)
SOUTH = Point(y_coord=-1, x_coord=0)
WEST = Point(y_coord=0, x_coord=-1)

@dataclass(frozen=True, order=True)
class Ferry:
    position: Point
    waypoint: Point

    def move(self, direction: Point, value: int) -> 'Ferry':
        return Ferry(self.position+(direction*value), self.waypoint)

    def move_waypoint(self, direction: Point, value: int) -> 'Ferry':
        return Ferry(self.position, self.waypoint+(direction*value))

    def turn_clockwise(self, turns: int) -> 'Ferry':
        waypoint = self.waypoint
        for _ in range(turns):
            waypoint = Point(waypoint.x_coord*-1, waypoint.y_coord)
        return Ferry(self.position, waypoint)

    def turn_left(self, degrees: int) -> 'Ferry':
        return self.turn_clockwise((360-degrees)//90)

    def turn_right(self, degrees: int) -> 'Ferry':
        return self.turn_clockwise(degrees//90)

    def follow_instruction(self, letter: str, value: int) -> 'Ferry':
        return {
            'N': self.move(NORTH, value),
            'E': self.move(EAST, value),
            'S': self.move(SOUTH, value),
            'W': self.move(WEST, value),
            'L': self.turn_left(value),
            'R': self.turn_right(value),
            'F': self.move(self.waypoint, value),
        }[letter]

    def follow_instructions(self, instructions: List[Tuple[str, int]]) -> 'Ferry':
        ferry = self
        for instruction in instructions:
            ferry = ferry.follow_instruction(*instruction)
        return ferry

    def follow_waypoint_instruction(self, letter: str, value: int) -> 'Ferry':
        return {
            'N': self.move_waypoint(NORTH, value),
            'E': self.move_waypoint(EAST, value),
            'S': self.move_waypoint(SOUTH, value),
            'W': self.move_waypoint(WEST, value),
            'L': self.turn_left(value),
            'R': self.turn_right(value),
            'F': self.move(self.waypoint, value),
        }[letter]

    def follow_waypoint_instructions(self, instructions: List[Tuple[str, int]]) -> 'Ferry':
        ferry = self
        for instruction in instructions:
            ferry = ferry.follow_waypoint_instruction(*instruction)
        return ferry

RE_INSTRUCTION = re.compile(r'(\w)(\d+)')
def read_instructions(text: str) -> List[Tuple[str, int]]:
    return [(letter, int(value)) for letter, value in RE_INSTRUCTION.findall(text)]

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2020, day=12)
    instructions = read_instructions(data)

    part1 = Ferry(Point(0, 0), EAST).follow_instructions(instructions)
    print(f'Part 1: {part1.position.manhattan_distance}')

    part2 = Ferry(Point(0, 0), Point(1, 10)).follow_waypoint_instructions(instructions)
    print(f'Part 2: {part2.position.manhattan_distance}')

if __name__ == '__main__':
    main()
