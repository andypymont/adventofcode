"""
2019 Day 3
https://adventofcode.com/2019/day/3
"""

from functools import reduce
from operator import __and__ as intersection
from typing import Dict, Iterable
import aocd # type: ignore

COMPASS: Dict[str, complex] = {
    'U': 0+1j,
    'D': 0-1j,
    'L': -1,
    'R': 1
}

def locations_visited(path: str) -> Dict[complex, int]:
    steps: int = 0
    location: complex = 0
    visited: Dict[complex, int] = {}
    for instruction in path.split(','):
        for _ in range(int(instruction[1:])):
            location += COMPASS[instruction[0]]
            steps += 1
            if location not in visited:
                visited[location] = steps
    return visited

def intersections(paths: Iterable[str]) -> Dict[complex, int]:
    visited = [locations_visited(path) for path in paths]
    intersects = reduce(
        intersection,
        [route.keys() for route in visited]
    )
    return {
        intersect: sum(route[intersect] for route in visited)
        for intersect in intersects
    }

def manhattan_distance(point: complex) -> int:
    return int(abs(point.real) + abs(point.imag))

def nearest(intersects: Dict[complex, int]) -> int:
    return min(manhattan_distance(point) for point in intersects)

def fewest_steps(intersects: Dict[complex, int]) -> int:
    return min(intersects.values())

def test_part1() -> None:
    """
    Examples for Part 1.
    """
    assert locations_visited('R8,U5,L5,D3').keys() == {
        1, 2, 3, 4, 5, 6, 7, 8, 8+1j, 8+2j, 8+3j, 8+4j, 8+5j, 7+5j, 6+5j, 5+5j, 4+5j, 3+5j,
        3+4j, 3+3j, 3+2j
    }
    assert intersections((
        'R8,U5,L5,D3',
        'U7,R6,D4,L4',
    )).keys() == {3+3j, 6+5j}
    assert nearest(intersections((
        'R75,D30,R83,U83,L12,D49,R71,U7,L72',
        'U62,R66,U55,R34,D71,R55,D58,R83',
    ))) == 159
    assert nearest(intersections((
        'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51',
        'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'
    ))) == 135

def test_part2() -> None:
    """
    Examples for Part 2.
    """
    assert fewest_steps(intersections((
        'R75,D30,R83,U83,L12,D49,R71,U7,L72',
        'U62,R66,U55,R34,D71,R55,D58,R83',
    ))) == 610
    assert fewest_steps(intersections((
        'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51',
        'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'
    ))) == 410

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2019, day=3)
    paths = data.split('\n')
    intersects = intersections(paths)

    print(f'Part 1: {nearest(intersects)}')
    print(f'Part 2: {fewest_steps(intersects)}')

if __name__ == '__main__':
    main()
