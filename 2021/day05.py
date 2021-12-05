"""
2021 Day 5
https://adventofcode.com/2021/day/5
"""

from collections import Counter
from itertools import chain
from typing import Iterable, Set, Tuple
import aocd # type: ignore

Line = Tuple[complex, complex]

def read_point(text: str) -> complex:
    numbers = [int(num) for num in text.split(',')]
    return complex(numbers[0], numbers[1])

def read_line(text:str) -> Line:
    points = [read_point(point) for point in text.split(' -> ')]
    if len(points) != 2:
        raise ValueError
    return (points[0], points[1])

def read_lines(text: str) -> Tuple[Line, ...]:
    return tuple(read_line(line) for line in text.split('\n'))

def gradient(line: Line) -> complex:
    start, finish = line
    return complex(
        1 if finish.real > start.real else 0 if finish.real == start.real else -1,
        1 if finish.imag > start.imag else 0 if finish.imag == start.imag else -1
    )

def points_visited(line: Line, discard_diagonals: bool = True) -> Set[complex]:
    location, finish = line
    grad = gradient(line)

    if discard_diagonals and grad not in (0+1j, 0-1j, 1+0j, -1+0j):
        return set()

    visited = set([location])

    while location != finish:
        location += grad
        visited.add(location)

    return visited

def overlapping_points(lines: Iterable[Line], discard_diagonals: bool = True) -> int:
    counts = Counter(chain(*(points_visited(line, discard_diagonals) for line in lines)))
    return sum(1 for occurrences in counts.values() if occurrences > 1)

def test_part1() -> None:
    """
    Examples for Part 1.
    """
    eg1 = '\n'.join((
        '0,9 -> 5,9',
        '8,0 -> 0,8',
        '9,4 -> 3,4',
        '2,2 -> 2,1',
        '7,0 -> 7,4',
        '6,4 -> 2,0',
        '0,9 -> 2,9',
        '3,4 -> 1,4',
        '0,0 -> 8,8',
        '5,5 -> 8,2',
    ))
    ex1 = (
        (0+9j, 5+9j),
        (8+0j, 0+8j),
        (9+4j, 3+4j),
        (2+2j, 2+1j),
        (7+0j, 7+4j),
        (6+4j, 2+0j),
        (0+9j, 2+9j),
        (3+4j, 1+4j),
        (0+0j, 8+8j),
        (5+5j, 8+2j)
    )
    assert read_lines(eg1) == ex1
    assert points_visited((1+1j, 1+3j)) == {1+1j, 1+2j, 1+3j}
    assert points_visited((9+7j, 7+7j)) == {9+7j, 8+7j, 7+7j}
    assert points_visited((1+1j, 5+5j)) == set()
    assert overlapping_points(ex1) == 5

def test_part2() -> None:
    """
    Examples for Part 2.
    """
    assert gradient((1+1j, 5+1j)) == 1+0j
    assert gradient((1+1j, 3+3j)) == 1+1j
    assert gradient((9+7j, 7+9j)) == -1+1j
    assert points_visited((1+1j, 3+3j), False) == {1+1j, 2+2j, 3+3j}
    assert points_visited((9+7j, 7+9j), False) == {9+7j, 8+8j, 7+9j}
    ex1 = (
        (0+9j, 5+9j),
        (8+0j, 0+8j),
        (9+4j, 3+4j),
        (2+2j, 2+1j),
        (7+0j, 7+4j),
        (6+4j, 2+0j),
        (0+9j, 2+9j),
        (3+4j, 1+4j),
        (0+0j, 8+8j),
        (5+5j, 8+2j)
    )
    assert overlapping_points(ex1, False) == 12

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2021, day=5)
    lines = read_lines(data)

    print(f'Part 1: {overlapping_points(lines)}')
    print(f'Part 2: {overlapping_points(lines, False)}')

if __name__ == '__main__':
    main()
