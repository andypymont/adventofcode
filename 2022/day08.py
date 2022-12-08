"""
2022 Day 8
https://adventofcode.com/2022/day/8
"""

from dataclasses import dataclass
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


@dataclass(frozen=True)
class TreeInfo:
    """
    The information about a tree: is it visible from the edge of the forest, and what is its scenic
    score.
    """

    visible: bool
    scenic_score: int

    @classmethod
    def from_tree(cls, forest: dict[Point, int], tree: Point) -> "TreeInfo":
        """
        Return the TreeInfo corresponding to the tree in the given position of the given forest.
        """
        visible = False
        scenic_score = 1

        for direction in (UP, DOWN, LEFT, RIGHT):
            target = tree
            distance = 0
            while True:
                target += direction
                if target not in forest:
                    visible = True
                    break
                distance += 1
                if forest[target] >= forest[tree]:
                    break
            scenic_score *= distance

        return cls(visible, scenic_score)

    @classmethod
    def all_from_forest(cls, forest: dict[Point, int]) -> dict[Point, "TreeInfo"]:
        """
        Return the TreeInfo for every tree in the given forest.
        """
        return {tree: cls.from_tree(forest, tree) for tree in forest}


def read_forest(text: str) -> dict[Point, int]:
    """
    Parse the puzzle input into a dictionary mapping locations to the tree height at the location.
    """
    return {
        Point(y, x): int(char)
        for y, line in enumerate(text.split("\n"))
        for x, char in enumerate(line)
    }


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

    assert TreeInfo.from_tree(forest, Point(1, 1)).visible
    assert TreeInfo.from_tree(forest, Point(1, 2)).visible
    assert not TreeInfo.from_tree(forest, Point(1, 3)).visible
    assert not TreeInfo.from_tree(forest, Point(2, 2)).visible

    tree_info = TreeInfo.all_from_forest(forest)
    assert sum(1 for tree in tree_info.values() if tree.visible) == 21


def test_part2() -> None:
    """
    Examples for Part 2.
    """
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

    assert TreeInfo.from_tree(forest, Point(1, 2)) == TreeInfo(True, 4)
    assert TreeInfo.from_tree(forest, Point(3, 2)) == TreeInfo(True, 8)

    info = TreeInfo.all_from_forest(forest)
    assert max(tree.scenic_score for tree in info.values()) == 8


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2022, day=8)

    forest = read_forest(data)
    info = TreeInfo.all_from_forest(forest)

    print(f"Part 1: {sum(1 for tree in info.values() if tree.visible)}")
    print(f"Part 2: {max(tree.scenic_score for tree in info.values())}")


if __name__ == "__main__":
    main()
