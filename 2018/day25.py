"""
2018 Day 25
https://adventofcode.com/2018/day/25
"""

from collections import deque
from itertools import permutations
from typing import Dict, Sequence, Set, Tuple
import aocd # type: ignore

Point = Tuple[int, int, int, int]

def manhattan_distance(first: Point, second: Point) -> int:
    return sum(
        abs(first[dimension] - second[dimension])
        for dimension in range(4)
    )

def read_point(line: str) -> Point:
    w, x, y, z, *_ = line.split(',')
    return (int(w), int(x), int(y), int(z))

def read_points(text: str) -> Sequence[Point]:
    return tuple(read_point(line) for line in text.split('\n'))

def connection_map(points: Sequence[Point]) -> Dict[Point, Set[Point]]:
    connections: Dict[Point, Set[Point]] = {}
    for first, second in permutations(points, 2):
        if first not in connections:
            connections[first] = set()
        if manhattan_distance(first, second) <= 3:
            connections[first].add(second)
    return connections

def all_reachable(conn_map: Dict[Point, Set[Point]], point: Point) -> Set[Point]:
    reachable = {point}
    explore: deque[Point] = deque(conn_map[point])
    while explore:
        consider = explore.popleft()
        reachable.add(consider)
        explore.extend(
            p for p in conn_map[consider] if p not in reachable
        )
    return reachable

def constellations(points: Sequence[Point]) -> int:
    count = 0
    mapped: Set[Point] = set()
    conn_map = connection_map(points)

    for point in points:
        if point not in mapped:
            count += 1
            mapped = mapped.union(all_reachable(conn_map, point))

    return count

def test_part1() -> None:
    """
    Examples for Part 1.
    """
    assert manhattan_distance(
        (0, 0, 0, 0),
        (3, 0, 0, 0)
    ) == 3
    assert manhattan_distance(
        (9, 0, 0, 0),
        (0, 3, 0, 0),
    ) == 12
    test_input = '\n'.join((
        '0,0,0,0',
        '3,0,0,0',
        '0,3,0,0',
        '0,0,3,0',
        '0,0,0,3',
        '0,0,0,6',
        '9,0,0,0',
        '12,0,0,0',
    ))
    test1 = (
        (0, 0, 0, 0),
        (3, 0, 0, 0),
        (0, 3, 0, 0),
        (0, 0, 3, 0),
        (0, 0, 0, 3),
        (0, 0, 0, 6),
        (9, 0, 0, 0),
        (12, 0, 0, 0),
    )
    assert read_points(test_input) == test1
    conn_map = connection_map(test1)
    assert all_reachable(conn_map, (0, 0, 0, 0)) == {
        (0, 0, 0, 0),
        (3, 0, 0, 0),
        (0, 3, 0, 0),
        (0, 0, 3, 0),
        (0, 0, 0, 3),
        (0, 0, 0, 6),
    }
    assert all_reachable(conn_map, (9, 0, 0, 0)) == {
        (9, 0, 0, 0),
        (12, 0, 0, 0),
    }
    assert constellations(test1) == 2
    test2 = (
        (-1, 2, 2, 0),
        (0, 0, 2, -2),
        (0, 0, 0, -2),
        (-1, 2, 0, 0),
        (-2, -2, -2, 2),
        (3, 0, 2, -1),
        (-1, 3, 2, 2),
        (-1, 0, -1, 0),
        (0, 2, 1, -2),
        (3, 0, 0, 0),
    )
    assert constellations(test2) == 4

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2018, day=25)
    points = read_points(data)
    print(f'Part 1: {constellations(points)}')

if __name__ == '__main__':
    main()
