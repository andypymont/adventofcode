"""
2022 Day 8
https://adventofcode.com/2022/day/8
"""

from dataclasses import dataclass
from functools import reduce
from operator import or_ as union
import aocd  # type: ignore


@dataclass(frozen=True, order=True)
class Point:
    """
    A two-dimensional point (y_coord, x_coord).
    """

    y_coord: int
    x_coord: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.y_coord + other.y_coord, self.x_coord + other.x_coord)


UP = Point(-1, 0)
DOWN = Point(1, 0)
LEFT = Point(0, -1)
RIGHT = Point(0, 1)


def read_forest(text: str) -> dict[Point, int]:
    """
    Parse the puzzle input into a dictionary mapping locations to the tree height at the location.
    """
    return {
        Point(y, x): int(char)
        for y, line in enumerate(text.split("\n"))
        for x, char in enumerate(line)
    }


def trees_visible_from(
    forest: dict[Point, int], tree: Point, direction: Point
) -> set[Point]:
    """
    Look from one tree on the edge of the forest toward the opposite edge and return a set of all
    visible trees.

    A tree is visible if all of the other trees between it and an edge of the forest are shorter
    than it.
    """
    visible = set()
    max_height = -1

    while tree in forest:
        height = forest[tree]
        if height > max_height:
            max_height = height
            visible.add(tree)
        tree += direction

    return visible


def visible_trees_in_forest(forest: dict[Point, int]) -> set[Point]:
    """
    Return the set of all visible trees looking from all edges of the given forest.
    """
    x_values = {pt.x_coord for pt in forest.keys()}
    y_values = {pt.y_coord for pt in forest.keys()}

    return reduce(
        union,
        (
            reduce(
                union, (trees_visible_from(forest, Point(0, x), DOWN) for x in x_values)
            ),
            reduce(
                union,
                (
                    trees_visible_from(forest, Point(max(y_values), x), UP)
                    for x in x_values
                ),
            ),
            reduce(
                union,
                (trees_visible_from(forest, Point(y, 0), RIGHT) for y in y_values),
            ),
            reduce(
                union,
                (
                    trees_visible_from(forest, Point(y, max(x_values)), LEFT)
                    for y in y_values
                ),
            ),
        ),
    )


def test_part1() -> None:
    """
    Examples for Part 1.
    """
    example = "\n".join(
        (
            "30373",
            "25512",
            "65332",
            "33549",
            "35390",
        )
    )
    forest = {
        Point(0, 0): 3,
        Point(0, 1): 0,
        Point(0, 2): 3,
        Point(0, 3): 7,
        Point(0, 4): 3,
        Point(1, 0): 2,
        Point(1, 1): 5,
        Point(1, 2): 5,
        Point(1, 3): 1,
        Point(1, 4): 2,
        Point(2, 0): 6,
        Point(2, 1): 5,
        Point(2, 2): 3,
        Point(2, 3): 3,
        Point(2, 4): 2,
        Point(3, 0): 3,
        Point(3, 1): 3,
        Point(3, 2): 5,
        Point(3, 3): 4,
        Point(3, 4): 9,
        Point(4, 0): 3,
        Point(4, 1): 5,
        Point(4, 2): 3,
        Point(4, 3): 9,
        Point(4, 4): 0,
    }
    assert read_forest(example) == forest
    assert trees_visible_from(forest, Point(0, 0), RIGHT) == {Point(0, 0), Point(0, 3)}
    assert len(visible_trees_in_forest(forest)) == 21


# def test_part2() -> None:
#     """
#     Examples for Part 2.
#     """
#     assert False


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2022, day=8)
    forest = read_forest(data)

    print(f"Part 1: {len(visible_trees_in_forest(forest))}")
    # print(f'Part 2: {p2}')


if __name__ == "__main__":
    main()
