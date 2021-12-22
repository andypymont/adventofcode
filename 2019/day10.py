"""
2019 Day 10
https://adventofcode.com/2019/day/10
"""

from collections import deque
from dataclasses import dataclass
from itertools import cycle
from typing import Dict, Iterable, Iterator, Set, Tuple
import aocd  # type: ignore
import numpy as np


@dataclass(frozen=True, order=True)
class Point:
    y: int
    x: int

    def __sub__(self, other: "Point") -> "Point":
        return self.__class__(
            self.y - other.y,
            self.x - other.x,
        )

    @property
    def angle(self) -> int:
        return int(np.arctan2(-self.x, self.y) / (np.pi * 2) * 36_000) % 360_000

    @property
    def distance(self) -> int:
        return int(100 * np.sqrt(self.y ** 2 + self.x ** 2))

    def visible_points(self, points: Iterable["Point"]) -> int:
        return len(self.targets(points))

    def targets(self, points: Iterable["Point"]) -> Dict[int, deque["Point"]]:
        locations: Dict[Tuple[int, int], Point] = {
            ((self - point).angle, (self - point).distance): point
            for point in points
            if point != self
        }
        targets: Dict[int, deque["Point"]] = {}
        for angle in {a for a, _ in locations}:
            distances = {dist for ang, dist in locations if ang == angle}
            targets[angle] = deque(
                locations[(angle, dist)] for dist in sorted(distances)
            )
        return targets


def read_asteroids(text: str) -> Set[Point]:
    asteroids = set()
    for y, row in enumerate(text.split("\n")):
        for x, char in enumerate(row):
            if char == "#":
                asteroids.add(Point(y, x))
    return asteroids


def best_station_visibility(asteroids: Iterable[Point]) -> Tuple[Point, int]:
    visibility = {
        asteroid: asteroid.visible_points(asteroids) for asteroid in asteroids
    }
    location = max(visibility, key=lambda loc: visibility[loc])
    return location, visibility[location]


def asteroids_destroyed(asteroids: Iterable[Point], station: Point) -> Iterator[Point]:
    targeting = station.targets(asteroids)
    for angle in cycle(sorted(targeting.keys())):
        aim = targeting[angle]
        if aim:
            yield aim.popleft()
        if sum(1 for queue in targeting.values() if queue) == 0:
            break


def test_part1() -> None:
    """
    Examples for Part 1.
    """
    text = "\n".join(
        (
            ".#..#",
            ".....",
            "#####",
            "....#",
            "...##",
        )
    )
    asteroids = {
        Point(0, 1),
        Point(0, 4),
        Point(2, 0),
        Point(2, 1),
        Point(2, 2),
        Point(2, 3),
        Point(2, 4),
        Point(3, 4),
        Point(4, 3),
        Point(4, 4),
    }
    assert read_asteroids(text) == asteroids
    assert Point(0, 1).visible_points(asteroids) == 7
    assert Point(2, 0).visible_points(asteroids) == 6
    assert Point(4, 3).visible_points(asteroids) == 8
    assert best_station_visibility(asteroids) == (Point(4, 3), 8)


def test_part2() -> None:
    """
    Examples for Part 2.
    """
    asteroids = {
        Point(0, 1),
        Point(0, 6),
        Point(0, 7),
        Point(0, 8),
        Point(0, 9),
        Point(0, 10),
        Point(0, 14),
        Point(1, 0),
        Point(1, 1),
        Point(1, 5),
        Point(1, 6),
        Point(1, 8),
        Point(1, 9),
        Point(1, 10),
        Point(1, 11),
        Point(1, 12),
        Point(1, 15),
        Point(1, 16),
        Point(2, 0),
        Point(2, 1),
        Point(2, 5),
        Point(2, 9),
        Point(2, 11),
        Point(2, 12),
        Point(2, 13),
        Point(2, 14),
        Point(2, 15),
        Point(3, 2),
        Point(3, 8),
        Point(3, 12),
        Point(3, 13),
        Point(3, 14),
        Point(4, 2),
        Point(4, 4),
        Point(4, 10),
        Point(4, 15),
        Point(4, 16),
    }
    destroyed = asteroids_destroyed(asteroids, Point(3, 8))
    assert next(destroyed) == Point(1, 8)
    assert next(destroyed) == Point(0, 9)
    assert next(destroyed) == Point(1, 9)
    assert next(destroyed) == Point(0, 10)
    assert next(destroyed) == Point(2, 9)
    assert next(destroyed) == Point(1, 11)
    assert next(destroyed) == Point(1, 12)
    assert next(destroyed) == Point(2, 11)
    assert next(destroyed) == Point(1, 15)

    asteroids = read_asteroids(
        "\n".join(
            (
                ".#..##.###...#######",
                "##.############..##.",
                ".#.######.########.#",
                ".###.#######.####.#.",
                "#####.##.#.##.###.##",
                "..#####..#.#########",
                "####################",
                "#.####....###.#.#.##",
                "##.#################",
                "#####.##.###..####..",
                "..######..##.#######",
                "####.##.####...##..#",
                ".#####..#.######.###",
                "##...#.##########...",
                "#.##########.#######",
                ".####.#.###.###.#.##",
                "....##.##.###..#####",
                ".#.#.###########.###",
                "#.#.#.#####.####.###",
                "###.##.####.##.#..##",
            )
        )
    )
    destroyed2 = list(asteroids_destroyed(asteroids, Point(13, 11)))
    assert destroyed2[0] == Point(12, 11)
    assert destroyed2[1] == Point(1, 12)
    assert destroyed2[2] == Point(2, 12)
    assert destroyed2[9] == Point(8, 12)
    assert destroyed2[19] == Point(0, 16)
    assert destroyed2[49] == Point(9, 16)
    assert destroyed2[99] == Point(16, 10)
    assert destroyed2[198] == Point(6, 9)
    assert destroyed2[199] == Point(2, 8)
    assert destroyed2[200] == Point(9, 10)


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2019, day=10)
    asteroids = read_asteroids(data)

    station, visible = best_station_visibility(asteroids)
    print(f"Part 1: {visible}")

    destroyed = asteroids_destroyed(asteroids, station)
    for _ in range(200):
        asteroid = next(destroyed)
    print(f"Part 2: {(asteroid.x * 100) + asteroid.y}")


if __name__ == "__main__":
    main()
