"""
2022 Day 12
https://adventofcode.com/2022/day/12
"""

from collections import deque
from dataclasses import dataclass
from string import ascii_lowercase
import aocd  # type: ignore

NORTH = complex(-1, 0)
EAST = complex(0, 1)
SOUTH = complex(1, 0)
WEST = complex(0, -1)
COMPASS = (NORTH, EAST, SOUTH, WEST)


@dataclass
class HeightMap:
    """
    A map of the heights and the starting and goal points.
    """

    heights: dict[complex, int]
    start: complex
    goal: complex

    @classmethod
    def from_input(cls, text: str) -> "HeightMap":
        """
        Read the HeightMap from the puzzle input.
        """
        heights: dict[complex, int] = {}
        start = goal = complex(0, 0)

        for y_coord, line in enumerate(text.split("\n")):
            for x_coord, char in enumerate(line):
                point = complex(y_coord, x_coord)
                if char == "S":
                    heights[point] = 0
                    start = point
                elif char == "E":
                    heights[point] = 25
                    goal = point
                else:
                    heights[point] = ascii_lowercase.index(char)

        return cls(heights, start, goal)

    def reachable_neighbours(self, point: complex) -> set[complex]:
        """
        Return all of the (orthogonal) reachable neighbours of the given point when tracing paths
        in REVERSE, i.e. those no more than one level lower.
        """
        height_limit = self.heights[point] - 1
        return set(
            neighbour
            for neighbour in (point + direction for direction in COMPASS)
            if self.heights.get(neighbour, -2) >= height_limit
        )

    def shortest_paths(self) -> tuple[int, int]:
        """
        Tracing from the destination, work down the mountain, finding and returning two values: the
        shortest path from the start to the goal point, and the shortest hiking trail, i.e. a route
        from height 0 to the summit.

        If either path cannot be found, return -1 instead.
        """
        visited: set[complex] = set()
        consider = deque([(self.goal, 0)])
        hiking = -1

        while consider:
            point, steps = consider.popleft()

            if point in visited:
                continue

            if hiking == -1 and self.heights[point] == 0:
                hiking = steps

            if point == self.start:
                return (steps, hiking)

            visited.add(point)

            for neighbour in self.reachable_neighbours(point):
                consider.append((neighbour, steps + 1))

        return (-1, hiking)


def test_parts_1_and_2() -> None:
    """
    Examples for Part 1.
    """
    height_map = HeightMap.from_input(
        "\n".join(
            (
                "Sabqponm",
                "abcryxxl",
                "accszExk",
                "acctuvwj",
                "abdefghi",
            )
        )
    )
    assert height_map.start == complex(0, 0)
    assert height_map.goal == complex(2, 5)
    assert height_map.heights[complex(0, 1)] == 0
    assert height_map.heights[complex(0, 2)] == 1
    assert height_map.heights[complex(0, 3)] == 16
    assert height_map.heights[complex(2, 4)] == 25
    assert height_map.reachable_neighbours(complex(0, 0)) == {
        complex(0, 1),
        complex(1, 0),
    }
    assert height_map.reachable_neighbours(complex(1, 1)) == {
        complex(0, 1),
        complex(2, 1),
        complex(1, 2),
        complex(1, 0),
    }
    assert height_map.reachable_neighbours(complex(0, 5)) == {
        complex(0, 4),
        complex(1, 5),
        complex(0, 6),
    }
    assert height_map.reachable_neighbours(complex(3, 4)) == {
        complex(2, 4),
        complex(3, 5),
        complex(3, 3),
    }
    assert height_map.shortest_paths() == (31, 29)


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2022, day=12)
    height_map = HeightMap.from_input(data)

    part_one, part_two = height_map.shortest_paths()
    print(f"Part 1: {part_one}")
    print(f"Part 2: {part_two}")


if __name__ == "__main__":
    main()
