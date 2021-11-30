"""
2018 Day 20
https://adventofcode.com/2018/day/20
"""

from collections import deque
from dataclasses import dataclass
from typing import Dict, Set, Tuple
import aocd # type: ignore

@dataclass(frozen=True)
class Point():
    y_coord: int
    x_coord: int

    def __add__(self, other: 'Point') -> 'Point':
        return Point(self.y_coord + other.y_coord, self.x_coord + other.x_coord)

directions = {
    'N': Point(-1, 0),
    'E': Point(0, 1),
    'S': Point(1, 0),
    'W': Point(0, -1),
}

Door = Tuple[Point, Point]

def find_all_doors(route_regex: str) -> Set[Door]:
    doors: Set[Tuple[Point, Point]] = set()
    pos = {Point(0, 0)}
    stack = []
    starts, ends = {Point(0, 0)}, set()

    for char in route_regex:
        if char == '|':
            # alternate route: update possible ending points and restart the group
            ends.update(pos)
            pos = starts
        elif char == '(':
            # start of group: add current positions as start of a new group
            stack.append((starts, ends))
            starts, ends = pos, set()
        elif char == ')':
            # end of group: finish current group, add current positions as possible ends
            pos.update(ends)
            starts, ends = stack.pop()
        elif char in directions:
            # move in a given direction from all possible current locations
            direction = directions[char]
            doors.update((p, p+direction) for p in pos)
            pos = {p+direction for p in pos}

    return doors

Reachability = Dict[Point, Set[Point]]

def reachability_dict(doors: Set[Door]) -> Reachability:
    reach: Reachability = {}

    for inside, outside in doors:
        if inside not in reach:
            reach[inside] = set()
        if outside not in reach:
            reach[outside] = set()
        reach[inside].add(outside)
        reach[outside].add(inside)

    return reach

def paths_to_rooms(reachability: Reachability) -> Dict[Point, int]:
    consider: deque[Tuple[Point, Set[Point]]] = deque()
    consider.append((Point(0, 0), set()))
    paths = {}

    while consider:
        location, visited = consider.popleft()
        paths[location] = len(visited)
        for next_step in reachability.get(location, set()):
            if next_step not in visited:
                consider.append((next_step, visited|{next_step}))

    return paths

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2018, day=20)

    doors = find_all_doors(data)
    reach = reachability_dict(doors)
    paths = paths_to_rooms(reach)

    print(f'Part 1: {max(paths.values())}')
    print(f'Part 2: {sum(1 for dist in paths.values() if dist >= 1000)}')

if __name__ == '__main__':
    main()
