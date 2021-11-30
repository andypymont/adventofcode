"""
2017 Day 19
https://adventofcode.com/2017/day/19
"""

from dataclasses import dataclass
from string import ascii_uppercase
from typing import Dict, Iterator, Sequence
import aocd # type: ignore

@dataclass(frozen=True)
class Point:
    y_coord: int
    x_coord: int

    def __add__(self, other: 'Point') -> 'Point':
        return Point(self.y_coord + other.y_coord, self.x_coord + other.x_coord)

    def __sub__(self, other: 'Point') -> 'Point':
        return Point(self.y_coord - other.y_coord, self.x_coord - other.x_coord)

    def neighbours(self) -> Iterator['Point']:
        yield self + Point(1, 0)
        yield self + Point(0, 1)
        yield self + Point(-1, 0)
        yield self + Point(0, -1)

Diagram = Dict[Point, str]
Journey = Sequence[Point]

def read_diagram(text: str) -> Diagram:
    diagram = {}
    for y_coord, line in enumerate(text.split('\n')):
        for x_coord, char in enumerate(line):
            if char != ' ':
                diagram[Point(y_coord, x_coord)] = char
    return diagram

def locate_start(diagram: Diagram) -> Point:
    return next(point for point in diagram.keys() if point.y_coord == 0)

def all_locations_on_journey(diagram: Diagram) -> Journey:
    visited = set()
    journey = []

    position = locate_start(diagram)
    direction = Point(1, 0)

    max_x = max(pt.x_coord for pt in diagram)
    max_y = max(pt.y_coord for pt in diagram)

    while all((
        position.x_coord >= 0,
        position.x_coord <= max_x,
        position.y_coord >= 0,
        position.y_coord <= max_y
    )):
        visited.add(position)
        journey.append(position)
        if diagram[position] == '+':
            neighbours = set(neighbour for neighbour in position.neighbours()
                             if (neighbour in diagram) and (neighbour not in visited))
            if not neighbours:
                return journey
            direction = next(iter(neighbours)) - position

        position += direction

    return journey

def letters_on_journey(journey: Journey, diagram: Diagram) -> str:
    characters = [diagram[location] for location in journey]
    return ''.join(char for char in characters if char in ascii_uppercase)

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2017, day=19)

    diagram = read_diagram(data)
    journey = all_locations_on_journey(diagram)

    print(f'Part 1: {letters_on_journey(journey, diagram)}')
    print(f'Part 2: {len(journey)}')

if __name__ == '__main__':
    main()
