"""
2018 Day 6
https://adventofcode.com/2018/day/6
"""

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Set, Tuple
import re
import aocd  # type: ignore

re_point = re.compile(r"(\d+), (\d+)")


@dataclass(frozen=True, order=True)
class Point:
    x_coord: int
    y_coord: int

    def distance(self, other: "Point") -> int:
        return abs(self.x_coord - other.x_coord) + abs(self.y_coord - other.y_coord)

    def distances(self, pointset: Iterable["Point"]) -> Dict["Point", int]:
        return dict((point, self.distance(point)) for point in pointset)

    def closest_to(self, pointset: Iterable["Point"]) -> Optional["Point"]:
        distances = self.distances(pointset)
        min_dist = min(distances.values())
        closest = [point for point in pointset if distances[point] == min_dist]
        if len(closest) == 1:
            return closest[0]
        return None

    def total_distance_to(self, pointset: Iterable["Point"]) -> int:
        distances = self.distances(pointset)
        return sum(distances.values())

    @classmethod
    def all_from_text(cls, text: str) -> Set["Point"]:
        return set(cls(*map(int, groups)) for groups in re_point.findall(text))

    @classmethod
    def constraints(cls, pointset: Iterable["Point"]) -> Tuple[int, int, int, int]:
        x_coord = [point.x_coord for point in pointset]
        y_coord = [point.y_coord for point in pointset]
        return (min(x_coord), min(y_coord), max(x_coord), max(y_coord))

    @classmethod
    def non_infinite_area_sizes(cls, pointset: Iterable["Point"]) -> List[int]:
        nia: Dict["Point", Set[Point]] = dict((point, set()) for point in pointset)
        infinite = set()

        minx, miny, maxx, maxy = cls.constraints(pointset)
        for x_coord in range(minx, maxx + 1):
            for y_coord in range(miny, maxy + 1):
                point = cls(x_coord, y_coord)
                closest = point.closest_to(pointset)
                if closest:
                    nia[closest].add(point)
                    if closest not in infinite:
                        if x_coord in (minx, maxx) or y_coord in (miny, maxy):
                            infinite.add(closest)

        return [len(nearby) for (point, nearby) in nia.items() if point not in infinite]

    @classmethod
    def total_distance_to_all_grid(
        cls, pointset: Iterable["Point"]
    ) -> Dict["Point", int]:
        grid = {}

        minx, miny, maxx, maxy = cls.constraints(pointset)
        for x_coord in range(minx, maxx + 1):
            for y_coord in range(miny, maxy + 1):
                point = cls(x_coord, y_coord)
                grid[point] = point.total_distance_to(pointset)

        return grid


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2018, day=6)
    points = Point.all_from_text(data)

    print(f"Part 1: {max(Point.non_infinite_area_sizes(points))}")

    distances = Point.total_distance_to_all_grid(points)
    print(f"Part 2: {sum(1 for (point, total) in distances.items() if total <= 10000)}")


if __name__ == "__main__":
    main()
