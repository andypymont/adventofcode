"""
2016 Day 24
https://adventofcode.com/2016/day/24
"""

from collections import deque
from dataclasses import dataclass
from itertools import combinations, permutations
from typing import Dict, Iterator, Sequence, Tuple
import aocd # type: ignore

@dataclass(frozen=True)
class Point():
    """
    A two-dimensional location with an x and a y coordinate.
    """
    x_coord: int
    y_coord: int

    def __add__(self, other: 'Point') -> 'Point':
        return Point(self.x_coord+other.x_coord, self.y_coord+other.y_coord)

class Map():
    """
    A map of the maze described in the puzzle input.
    """

    def __init__(self, text: str):
        rows = text.split('\n')
        self.y_size = len(rows)
        self.x_size = len(rows[0])
        self.walls = set()
        self.poi = {}
        for y_coord, row in enumerate(rows):
            for x_coord, char in enumerate(row):
                if char == '#':
                    self.walls.add(Point(x_coord, y_coord))
                elif char != '.':
                    self.poi[int(char)] = Point(x_coord, y_coord)

    def all_possible_moves(self, location: Point) -> Iterator[Point]:
        """
        Yield each possible move from the given location.
        """
        for direction in (Point(1, 0), Point(-1, 0), Point(0, 1), Point(0, -1)):
            new_location = location + direction
            if (0 <= new_location.x_coord <= self.x_size
                and 0 <= new_location.y_coord <= self.y_size
                and new_location not in self.walls):
                yield new_location

    def shortest_path(self, start: Point, finish: Point) -> int:
        """
        Calculate the shortest path between the two given points.
        """
        visited = set()
        search = deque([[start]])

        while search:
            route = search.popleft()
            location = route[-1]
            if location == finish:
                return len(route) - 1
            if location not in visited:
                visited.add(location)
                search.extend(route + [newloc] for newloc in self.all_possible_moves(location))

        return -1

    def poi_routes(self) -> Dict[Tuple[int, int], int]:
        """
        Calculate the shortest path between each pair of POI in the maze, and return a dictionary
        mapping each pair to the distance of the shortest path.
        """
        routes = {}
        for (first, second) in combinations(self.poi.keys(), 2):
            dist = self.shortest_path(self.poi[first], self.poi[second])
            routes[(first, second)] = dist
            routes[(second, first)] = dist
        return routes

def journey_length(poi_routes: Dict[Tuple[int, int], int], journey: Sequence[int]) -> int:
    """
    Calculate the total length of a journey that visits the POI in the order described in
    'journey'.
    """
    return sum(poi_routes[(journey[x], journey[x+1])] for x in range(len(journey)-1))

def shortest_journey(maze: Map, comeback: bool = False) -> int:
    """
    Find the shortest journey for the given maze, visiting all POI and, if 'comeback' is True,
    also returning to the start point.
    """
    poi_routes = maze.poi_routes()
    journeys = [
        [0] + list(perm) + ([0] if comeback else [])
        for perm in permutations(poi for poi in maze.poi.keys() if poi != 0)
    ]
    return min(journey_length(poi_routes, journey) for journey in journeys)

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2016, day=24)
    maze = Map(data)

    print(f'Part 1: {shortest_journey(maze)}')
    print(f'Part 2: {shortest_journey(maze, comeback=True)}')

if __name__ == '__main__':
    main()
