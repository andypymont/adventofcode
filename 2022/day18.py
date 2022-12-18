"""
2022 Day 18
https://adventofcode.com/2022/day/18
"""

from collections import deque
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


def exterior_surface_area(cubes: set[Cube]) -> int:
    """
    Calculate the exterior surface area of the structure.
    """
    min_x = min(c.x_coord for c in cubes) - 1
    min_y = min(c.y_coord for c in cubes) - 1
    min_z = min(c.z_coord for c in cubes) - 1
    max_x = max(c.x_coord for c in cubes) + 1
    max_y = max(c.y_coord for c in cubes) + 1
    max_z = max(c.z_coord for c in cubes) + 1

    start = Cube(min_x, min_y, min_z)
    surface: set[tuple[Cube, Cube]] = set()
    visited: set[Cube] = set()
    consider: deque[tuple[Cube, Cube]] = deque([(start, start)])

    while consider:
        cube, prev = consider.popleft()

        # if we're in a cube, we have hit it moving from our previous position: record that
        if cube in cubes:
            surface.add((cube, prev))
            continue

        # check if we've been here before and if not, record this position for future checks
        if cube in visited:
            continue
        visited.add(cube)

        # stop if we're too far from the structure
        if cube.x_coord < start.x_coord or cube.x_coord > max_x:
            continue
        if cube.y_coord < start.y_coord or cube.y_coord > max_y:
            continue
        if cube.z_coord < start.z_coord or cube.z_coord > max_z:
            continue

        # now consider next neighbours from here
        for neighbour in cube.neighbours():
            consider.append((neighbour, cube))

    return len(surface)


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


def test_part2() -> None:
    """
    Examples for Part 2.
    """
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
    assert exterior_surface_area(cubes) == 58


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2022, day=18)
    cubes = Cube.all_from_text(data)

    print(f"Part 1: {surface_area(cubes)}")
    print(f"Part 2: {exterior_surface_area(cubes)}")


if __name__ == "__main__":
    main()
