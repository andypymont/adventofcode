"""
2018 Day 17
https://adventofcode.com/2018/day/17
"""

from collections import deque
from typing import Set, Tuple
import aocd # type: ignore
import regex as re # type: ignore

RE_VERTICAL = re.compile(r'x=(\d+), y=(\d+)..(\d+)')
RE_HORIZONTAL = re.compile(r'y=(\d+), x=(\d+)..(\d+)')

def read_sand(text: str) -> Set[complex]:
    sand = set()

    for x_coord, min_y, max_y in [tuple(map(int, val)) for val in RE_VERTICAL.findall(text)]:
        for y_coord in range(min_y, max_y+1):
            sand.add(complex(x_coord, y_coord))

    for y_coord, min_x, max_x in [tuple(map(int, val)) for val in RE_HORIZONTAL.findall(text)]:
        for x_coord in range(min_x, max_x+1):
            sand.add(complex(x_coord, y_coord))

    return sand

UP = -1j
DOWN = 1j
LEFT = -1
RIGHT = 1

def fill_horizontally(start: complex, occupied: Set[complex], water: Set[complex]) -> bool:
    y_coord = start.imag
    occ_in_row = {int(o.real) for o in occupied if o.imag == y_coord}

    if not occ_in_row:
        return False

    min_x = min(x for x in occ_in_row)
    max_x = max(x for x in occ_in_row)

    x_coord = int(start.real)
    if min_x > x_coord or max_x < x_coord:
        return False

    while x_coord > min_x:
        if complex(x_coord, y_coord+1) not in occupied:
            return False
        if complex(x_coord-1, y_coord) in occupied:
            min_x = x_coord
        x_coord -= 1

    x_coord = int(start.real)
    while x_coord < max_x:
        if complex(x_coord, y_coord+1) not in occupied:
            return False
        if complex(x_coord+1, y_coord) in occupied:
            max_x = x_coord
        x_coord += 1

    for x_coord in range(min_x, max_x+1):
        water.add(complex(x_coord, y_coord))
    return True

def flow(sand: Set[complex]) -> Tuple[Set[complex], Set[complex]]:
    min_y = min(s.imag for s in sand)
    max_y = max(s.imag for s in sand)

    flows: deque[Tuple[complex, complex]] = deque()
    flows.append((DOWN, 500))
    visited = set()
    water: Set[complex] = set()

    while flows:
        direct, pos = flows.popleft()

        if (direct, pos) not in flows:
            visited.add(pos)
            occupied = sand.union(water)

            if direct == DOWN:
                if pos + DOWN in occupied:
                    if fill_horizontally(pos, occupied, water):
                        flows.append((DOWN, pos+UP))
                    else:
                        flows.append((LEFT, pos))
                        flows.append((RIGHT, pos))
                elif (pos + DOWN).imag <= max_y:
                    flows.append((DOWN, pos+DOWN))

            elif (pos + DOWN) not in occupied:
                flows.append((DOWN, pos))

            elif (pos + direct) not in occupied:
                flows.append((direct, pos + direct))

    visited = {i for i in visited if i.imag >= min_y}
    return water, visited

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2018, day=17)
    sand = read_sand(data)

    stationary, flowing = flow(sand)
    print(f'Part 1: {len(stationary.union(flowing))}')
    print(f'Part 2: {len(stationary)}')

if __name__ == '__main__':
    main()
