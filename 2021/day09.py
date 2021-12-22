"""
2021 Day 9
https://adventofcode.com/2021/day/9
"""

from collections import deque
from math import inf, prod
from typing import Dict, Set
import aocd  # type: ignore


def read_heightmap(text: str) -> Dict[complex, int]:
    heightmap: Dict[complex, int] = {}

    for y, line in enumerate(text.split("\n")):
        for x, value in enumerate(line):
            heightmap[complex(x, y)] = int(value)

    return heightmap


def is_low_point(point: complex, heightmap: Dict[complex, int]) -> bool:
    return heightmap[point] < min(
        heightmap.get(point + dir, inf) for dir in (0 - 1j, 1 + 0j, 0 + 1j, -1 + 0j)
    )


def low_points(heightmap: Dict[complex, int]) -> Set[complex]:
    return {pt for pt in heightmap if is_low_point(pt, heightmap)}


def basin_size(heightmap: Dict[complex, int], lowpoint: complex) -> int:
    basin: Set[complex] = set()
    explore: deque[complex] = deque([lowpoint])

    while explore:
        location = explore.popleft()
        basin.add(location)
        explore.extend(
            neighbour
            for neighbour in [
                location + direction for direction in (0 - 1j, 1 + 0j, 0 + 1j, -1 + 0j)
            ]
            if heightmap.get(neighbour, 9) != 9 and neighbour not in basin
        )

    return len(basin)


def test_part1() -> None:
    """
    Examples for Part 1.
    """
    text = "\n".join(
        (
            "2199943210",
            "3987894921",
            "9856789892",
            "8767896789",
            "9899965678",
        )
    )
    heightmap = {
        0 + 0j: 2,
        1 + 0j: 1,
        2 + 0j: 9,
        3 + 0j: 9,
        4 + 0j: 9,
        5 + 0j: 4,
        6 + 0j: 3,
        7 + 0j: 2,
        8 + 0j: 1,
        9 + 0j: 0,
        0 + 1j: 3,
        1 + 1j: 9,
        2 + 1j: 8,
        3 + 1j: 7,
        4 + 1j: 8,
        5 + 1j: 9,
        6 + 1j: 4,
        7 + 1j: 9,
        8 + 1j: 2,
        9 + 1j: 1,
        0 + 2j: 9,
        1 + 2j: 8,
        2 + 2j: 5,
        3 + 2j: 6,
        4 + 2j: 7,
        5 + 2j: 8,
        6 + 2j: 9,
        7 + 2j: 8,
        8 + 2j: 9,
        9 + 2j: 2,
        0 + 3j: 8,
        1 + 3j: 7,
        2 + 3j: 6,
        3 + 3j: 7,
        4 + 3j: 8,
        5 + 3j: 9,
        6 + 3j: 6,
        7 + 3j: 7,
        8 + 3j: 8,
        9 + 3j: 9,
        0 + 4j: 9,
        1 + 4j: 8,
        2 + 4j: 9,
        3 + 4j: 9,
        4 + 4j: 9,
        5 + 4j: 6,
        6 + 4j: 5,
        7 + 4j: 6,
        8 + 4j: 7,
        9 + 4j: 8,
    }
    assert read_heightmap(text) == heightmap
    assert low_points(heightmap) == {1 + 0j, 9 + 0j, 2 + 2j, 6 + 4j}
    assert sum(1 + heightmap[lp] for lp in low_points(heightmap)) == 15


def test_part2() -> None:
    """
    Examples for Part 2.
    """
    heightmap = {
        0 + 0j: 2,
        1 + 0j: 1,
        2 + 0j: 9,
        3 + 0j: 9,
        4 + 0j: 9,
        5 + 0j: 4,
        6 + 0j: 3,
        7 + 0j: 2,
        8 + 0j: 1,
        9 + 0j: 0,
        0 + 1j: 3,
        1 + 1j: 9,
        2 + 1j: 8,
        3 + 1j: 7,
        4 + 1j: 8,
        5 + 1j: 9,
        6 + 1j: 4,
        7 + 1j: 9,
        8 + 1j: 2,
        9 + 1j: 1,
        0 + 2j: 9,
        1 + 2j: 8,
        2 + 2j: 5,
        3 + 2j: 6,
        4 + 2j: 7,
        5 + 2j: 8,
        6 + 2j: 9,
        7 + 2j: 8,
        8 + 2j: 9,
        9 + 2j: 2,
        0 + 3j: 8,
        1 + 3j: 7,
        2 + 3j: 6,
        3 + 3j: 7,
        4 + 3j: 8,
        5 + 3j: 9,
        6 + 3j: 6,
        7 + 3j: 7,
        8 + 3j: 8,
        9 + 3j: 9,
        0 + 4j: 9,
        1 + 4j: 8,
        2 + 4j: 9,
        3 + 4j: 9,
        4 + 4j: 9,
        5 + 4j: 6,
        6 + 4j: 5,
        7 + 4j: 6,
        8 + 4j: 7,
        9 + 4j: 8,
    }
    assert basin_size(heightmap, 1 + 0j) == 3
    assert basin_size(heightmap, 9 + 0j) == 9
    assert basin_size(heightmap, 2 + 2j) == 14
    assert basin_size(heightmap, 6 + 4j) == 9
    assert prod(sorted((3, 9, 14, 9), reverse=True)[:3]) == 1134


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2021, day=9)
    heightmap = read_heightmap(data)

    low = low_points(heightmap)
    part1 = sum(1 + heightmap[lp] for lp in low)
    print(f"Part 1: {part1}")

    basins = [basin_size(heightmap, lp) for lp in low]
    part2 = prod(sorted(basins, reverse=True)[:3])
    print(f"Part 2: {part2}")


if __name__ == "__main__":
    main()
