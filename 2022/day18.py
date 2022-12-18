"""
2022 Day 18
https://adventofcode.com/2022/day/18
"""

from dataclasses import dataclass
from typing import Iterator
import aocd  # type: ignore


@dataclass(frozen=True, order=True)
class Cube:
    """
    A 1x1x1 cube located in three-dimensional space.
    """

    x_coord: int
    y_coord: int
    z_coord: int

    @classmethod
    def from_text(cls, line: str) -> "Cube":
        """
        Read a Cube from a single line of the puzzle input.
        """
        coords = [int(x) for x in line.split(",")]
        return cls(coords[0], coords[1], coords[2])

    @classmethod
    def all_from_text(cls, text: str) -> set["Cube"]:
        """
        Read the set of Cubes from the puzzle input.
        """
        return {Cube.from_text(line) for line in text.splitlines()}

    def __add__(self, other: "Cube") -> "Cube":
        return Cube(
            self.x_coord + other.x_coord,
            self.y_coord + other.y_coord,
            self.z_coord + other.z_coord,
        )

    def neighbours(self) -> Iterator["Cube"]:
        """
        Yield each neighbour of this cube (as reached through one of its 6 faces)
        """
        yield self + Cube(1, 0, 0)
        yield self + Cube(-1, 0, 0)
        yield self + Cube(0, 1, 0)
        yield self + Cube(0, -1, 0)
        yield self + Cube(0, 0, 1)
        yield self + Cube(0, 0, -1)


def surface_area(cubes: set[Cube]) -> int:
    """
    Calculate the surface area of the structure, i.e. all cube faces which do not directly contact
    another cube.
    """
    surface = 0
    for cube in cubes:
        for neighbour in cube.neighbours():
            if neighbour not in cubes:
                surface += 1

    return surface


def test_part1() -> None:
    """
    Examples for Part 1.
    """
    assert Cube.from_text("2,2,2") == Cube(2, 2, 2)
    assert Cube.from_text("2,3,2") == Cube(2, 3, 2)
    assert Cube.from_text("1,2,5") == Cube(1, 2, 5)

    cubes = {
        Cube(2, 2, 2),
        Cube(1, 2, 2),
        Cube(3, 2, 2),
        Cube(2, 1, 2),
        Cube(2, 3, 2),
        Cube(2, 2, 1),
        Cube(2, 2, 3),
        Cube(2, 2, 4),
        Cube(2, 2, 6),
        Cube(1, 2, 5),
        Cube(3, 2, 5),
        Cube(2, 1, 5),
        Cube(2, 3, 5),
    }
    assert (
        Cube.all_from_text(
            "\n".join(
                (
                    "2,2,2",
                    "1,2,2",
                    "3,2,2",
                    "2,1,2",
                    "2,3,2",
                    "2,2,1",
                    "2,2,3",
                    "2,2,4",
                    "2,2,6",
                    "1,2,5",
                    "3,2,5",
                    "2,1,5",
                    "2,3,5",
                )
            )
        )
        == cubes
    )
    assert set(Cube(2, 2, 6).neighbours()) == {
        Cube(1, 2, 6),
        Cube(3, 2, 6),
        Cube(2, 1, 6),
        Cube(2, 3, 6),
        Cube(2, 2, 5),
        Cube(2, 2, 7),
    }

    assert surface_area(cubes) == 64


# def test_part2() -> None:
#     """
#     Examples for Part 2.
#     """
#     assert False


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2022, day=18)
    cubes = Cube.all_from_text(data)

    print(f"Part 1: {surface_area(cubes)}")
    # print(f'Part 2: {p2}')


if __name__ == "__main__":
    main()
