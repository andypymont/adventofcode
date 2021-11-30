"""
2020 Day 11
https://adventofcode.com/2020/day/11
"""
from dataclasses import dataclass
from typing import Dict, Set
import aocd # type: ignore

@dataclass(frozen=True)
class Point():
    y_coord: int
    x_coord: int

    def __add__(self, other: 'Point') -> 'Point':
        return Point(self.y_coord+other.y_coord, self.x_coord+other.x_coord)

@dataclass(frozen=True)
class Seat():
    location: Point
    occupied: bool
    neighbours: Set[Point]

    @classmethod
    def all_from_input(cls, text: str, neighbour_policy: str = 'adjacent') -> Dict[Point, 'Seat']:
        lines = text.split('\n')

        points = {}
        for y_coord, line in enumerate(lines):
            for x_coord, char in enumerate(line):
                if char != '.':
                    points[Point(y_coord, x_coord)] = (char == '#')

        neighbours: Dict[Point, Set[Point]] = {}

        for point in points:
            max_x = max(point.x_coord for point in points)
            max_y = max(point.y_coord for point in points)
            neighbours[point] = set()
            for compass in (
                Point(-1, -1), Point(-1, 0), Point(-1, 1),
                Point(0, -1), Point(0, 1),
                Point(1, -1), Point(1, 0), Point(1, 1),
            ):
                nearby = point + compass
                if neighbour_policy == 'nearest':
                    while (nearby not in points and nearby.x_coord >= 0 and nearby.y_coord >= 0
                           and nearby.x_coord <= max_x and nearby.y_coord <= max_y):
                        nearby += compass
                if nearby in points:
                    neighbours[point].add(nearby)

        return {
            point: cls(point, occupied, neighbours.get(point, set()))
            for point, occupied in points.items()
        }

    def occupied_neighbours(self, seats: Dict[Point, 'Seat']) -> int:
        return sum(1 for neighbour in self.neighbours if seats[neighbour].occupied)

    def progress(self, seats: Dict[Point, 'Seat'], occupied_tolerance: int = 4) -> 'Seat':
        if (not self.occupied) and self.occupied_neighbours(seats) == 0:
            return Seat(self.location, True, self.neighbours)
        if self.occupied and self.occupied_neighbours(seats) >= occupied_tolerance:
            return Seat(self.location, False, self.neighbours)

        return Seat(self.location, self.occupied, self.neighbours)

def progress_until_stable(
    seats: Dict[Point, 'Seat'],
    occupied_tolerance: int = 4
) -> Dict[Point, 'Seat']:
    oldseats = ""
    while oldseats != repr(seats):
        oldseats = repr(seats)
        seats = {
            point: seat.progress(seats, occupied_tolerance) for point, seat in seats.items()
        }
    return seats

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2020, day=11)

    seats = Seat.all_from_input(data)
    stable = progress_until_stable(seats)
    part1 = sum(1 for seat in stable.values() if seat.occupied)
    print(f'Part 1: {part1}')

    seats = Seat.all_from_input(data, 'nearest')
    stable = progress_until_stable(seats, occupied_tolerance=5)
    part2 = sum(1 for seat in stable.values() if seat.occupied)
    print(f'Part 2: {part2}')

if __name__ == '__main__':
    main()
