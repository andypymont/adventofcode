"""
2016 Day 1
https://adventofcode.com/2016/day/1
"""

from dataclasses import dataclass
from typing import Dict, Iterable, Iterator, Sequence
import aocd # type: ignore
import regex as re # type: ignore

@dataclass(frozen=True)
class Coordinate():
    """
    Simple 2d coordinate with x and y values.
    """
    x: int
    y: int

    def __add__(self, other: 'Coordinate') -> 'Coordinate':
        return self.__class__(self.x + other.x, self.y + other.y)

    @property
    def taxicab_distance(self) -> int:
        """
        Taxicab distance (i.e. absolute X distance plus absolute Y distance) of this coordinate
        from the origin.
        """
        return abs(self.x) + abs(self.y)

WEST = Coordinate(-1, 0)
EAST = Coordinate(1, 0)
NORTH = Coordinate(0, 1)
SOUTH = Coordinate(0, -1)
TURN_LEFT: Dict[Coordinate, Coordinate] = {
    WEST: SOUTH,
    SOUTH: EAST,
    EAST: NORTH,
    NORTH: WEST
}
TURN_RIGHT: Dict[Coordinate, Coordinate] = {
    WEST: NORTH,
    NORTH: EAST,
    EAST: SOUTH,
    SOUTH: WEST
}

def journey(instructions: str) -> Sequence[Coordinate]:
    """
    Translate a string of L/R instructions into a sequence of locations visited on a journey
    following those instructions.
    """
    locations = [Coordinate(0, 0)]
    facing = NORTH
    for (turn, dist) in re.findall(r'([RL])(\d+)', instructions):
        facing = TURN_LEFT[facing] if turn == 'L' else TURN_RIGHT[facing]
        for _ in range(int(dist)):
            locations.append(locations[-1] + facing)
    return locations

def revisited_coordinates(sequence: Iterable[Coordinate]) -> Iterator[Coordinate]:
    """
    Filter an iterable of Coordinates, returning only those which are repeated visits.
    """
    visited = set()
    for item in sequence:
        if item in visited:
            yield item
        visited.add(item)

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2016, day=1)
    locations = journey(data)

    print(f'Part 1: {locations[-1].taxicab_distance}')
    first_repeat = next(revisited_coordinates(locations))
    print(f'Part 2: {first_repeat.taxicab_distance}')

if __name__ == '__main__':
    main()
