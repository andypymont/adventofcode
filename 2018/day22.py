"""
2018 Day 22
https://adventofcode.com/2018/day/22
"""

from dataclasses import dataclass
from heapq import heapify, heappush, heappop
from typing import Dict, Iterable, Iterator, Sequence, Tuple
import aocd # type: ignore
import regex as re # type: ignore

@dataclass(frozen=True, order=True)
class Point():
    y_coord: int
    x_coord: int

    @classmethod
    def from_regex_groups(cls, groups: Sequence[str]) -> 'Point':
        x_coord, y_coord = [int(val) for val in groups]
        return cls(y_coord, x_coord)

    def __add__(self, other: 'Point') -> 'Point':
        return Point(self.y_coord + other.y_coord, self.x_coord + other.x_coord)

    @property
    def neighbours(self) -> Sequence['Point']:
        neighbours = [
            self + direction for direction in (
                Point(-1, 0),
                Point(0, 1),
                Point(1, 0),
                Point(0, -1)
            )
        ]
        return [
            neighbour for neighbour in neighbours
            if neighbour.x_coord >=0 and neighbour.y_coord >= 0
        ]

@dataclass(frozen=True)
class Region():
    position: Point
    geologic_index: int
    depth: int

    @classmethod
    def extend_cave_system(cls, location: Point, cave_system: 'CaveSystem') -> 'Region':
        geologic_index = 0

        if location != Point(0, 0) and location != cave_system.target:
            if location.y_coord == 0:
                geologic_index = location.x_coord * 16807
            elif location.x_coord == 0:
                geologic_index = location.y_coord * 48271
            else:
                west = cave_system.get(Point(location.y_coord, location.x_coord-1))
                north = cave_system.get(Point(location.y_coord-1, location.x_coord))
                geologic_index = west.erosion_level * north.erosion_level

        region = cls(location, geologic_index, cave_system.depth)
        cave_system.system[location] = region
        return region

    @property
    def erosion_level(self) -> int:
        return (self.geologic_index + self.depth) % 20183

    @property
    def risk_level(self) -> int:
        return self.erosion_level % 3

    @property
    def terrain(self) -> str:
        return ('rocky', 'wet', 'narrow')[self.risk_level]

@dataclass
class CaveSystem():
    system: Dict[Point, Region]
    target: Point
    depth: int

    @property
    def risk_level(self) -> int:
        return sum(region.risk_level for region in self.system.values())

    def get(self, location: Point) -> Region:
        if location in self.system:
            return self.system[location]
        return self.add(
            Point(max(location.y_coord, 0), max(location.x_coord, 0))
        )

    def add(self, location: Point) -> Region:
        geologic_index = 0

        if location != Point(0, 0) and location != self.target:
            if location.y_coord == 0:
                geologic_index = location.x_coord * 16807
            elif location.x_coord == 0:
                geologic_index = location.y_coord * 48271
            else:
                west = self.get(Point(location.y_coord, location.x_coord-1))
                north = self.get(Point(location.y_coord-1, location.x_coord))
                geologic_index = west.erosion_level * north.erosion_level

        region = Region(location, geologic_index, self.depth)
        self.system[location] = region
        return region

    def extend(self) -> None:
        for location in (
            Point(y, x) for x in range(self.target.x_coord+1)
            for y in range(self.target.y_coord+1)
        ):
            self.add(location)

INACCESSIBLE_TERRAIN = {
    'climbing gear': 'narrow',
    'torch': 'wet',
    'neither': 'rocky'
}

@dataclass(frozen=True, order=True)
class Equipment():
    name: str

    @property
    def inaccessible_terrain(self) -> str:
        return INACCESSIBLE_TERRAIN[self.name]

    def is_valid_in_terrain(self, terrain: str) -> bool:
        return terrain != self.inaccessible_terrain

    def switch(self, terrain: str) -> 'Equipment':
        return next(
            Equipment(equip) for equip, inaccess in INACCESSIBLE_TERRAIN.items()
            if equip != self.name and inaccess != terrain
        )

@dataclass(frozen=True, order=True)
class SearchState():
    minutes: int
    position: Point
    equipment: Equipment

    @classmethod
    def initial_state(cls) -> 'SearchState':
        return cls(0, Point(0, 0), Equipment('climbing gear'))

    def accessible_neighbours(self, cave_system: CaveSystem) -> Iterable[Point]:
        return (
            loc for loc in self.position.neighbours
            if self.equipment.is_valid_in_terrain(cave_system.get(loc).terrain)
        )

    def possible_next_steps(self, cave_system: CaveSystem) -> Iterator['SearchState']:
        for location in self.accessible_neighbours(cave_system):
            yield SearchState(self.minutes + 1, location, self.equipment)

        equip = self.equipment.switch(cave_system.get(self.position).terrain)
        yield SearchState(self.minutes + 7, self.position, equip)

def find_shortest_route(cave: CaveSystem) -> int:
    best_routes: Dict[Tuple[Point, Equipment], int] = {}
    queue = [SearchState.initial_state()]
    heapify(queue)

    while len(queue) > 0:
        state = heappop(queue)

        if state.position == cave.target:
            return state.minutes

        best_key = (state.position, state.equipment)
        if (best_key not in best_routes) or state.minutes < best_routes[best_key]:
            best_routes[best_key] = state.minutes
            for move in state.possible_next_steps(cave):
                heappush(queue, move)

    return -1

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2018, day=22)

    depth = int(re.compile(r'depth: (\d+)').findall(data)[0])
    target = Point.from_regex_groups(re.compile(r'target: (\d+),(\d+)').findall(data)[0])

    cave = CaveSystem({}, target, depth)
    cave.extend()
    print(f'Part 1: {cave.risk_level}')

    print(f'Part 2: {find_shortest_route(cave)}')

if __name__ == '__main__':
    main()
