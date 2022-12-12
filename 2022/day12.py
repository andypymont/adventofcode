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
        Return all of the (orthogonal) reachable neighbours of the given point, i.e. those no more
        than one level higher.
        """
        height_limit = self.heights[point] + 1
        return set(
            neighbour
            for neighbour in (point + direction for direction in COMPASS)
            if self.heights.get(neighbour, 30) <= height_limit
        )

    def shortest_path(self) -> int:
        """
        Calculate the shortest path from the start to the goal point and return the number of steps
        taken.
        """
        visited: set[complex] = set()
        consider = deque([(self.start, 0)])

        while consider:
            point, steps = consider.popleft()

            if point in visited:
                continue

            if point == self.goal:
                return steps

            visited.add(point)

            for neighbour in self.reachable_neighbours(point):
                consider.append((neighbour, steps + 1))

        raise ValueError("No valid route found")


def test_part1() -> None:
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
        complex(0, 6),
    }
    assert height_map.reachable_neighbours(complex(3, 4)) == {
        complex(3, 5),
        complex(4, 4),
        complex(3, 3),
    }
    assert height_map.shortest_path() == 31


# def test_part2() -> None:
#     """
#     Examples for Part 2.
#     """
#     assert False


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2022, day=12)
    height_map = HeightMap.from_input(data)

    print(f"Part 1: {height_map.shortest_path()}")
    # print(f'Part 2: {p2}')


if __name__ == "__main__":
    main()
