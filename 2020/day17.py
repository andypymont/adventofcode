"""
2020 Day 17
https://adventofcode.com/2020/day/17
"""

from dataclasses import dataclass
from functools import reduce
from operator import __or__ as union
from typing import Set, Union
import aocd  # type: ignore


@dataclass(frozen=True, order=True)
class Cube:
    z_coord: int
    y_coord: int
    x_coord: int

    @property
    def adjacent(self) -> Set["Simulatable"]:
        return set(
            Cube(self.z_coord + dz, self.y_coord + dy, self.x_coord + dx)
            for dz in range(-1, 2)
            for dy in range(-1, 2)
            for dx in range(-1, 2)
            if not dz == dy == dx == 0
        )

    def active(self, previous_state: Set["Simulatable"]) -> bool:
        active_neighbours = sum(
            1 for neighbour in self.adjacent if neighbour in previous_state
        )
        if self in previous_state:
            return active_neighbours in (2, 3)
        return active_neighbours == 3


@dataclass(frozen=True, order=True)
class Tesseract:
    w_coord: int
    z_coord: int
    y_coord: int
    x_coord: int

    @property
    def adjacent(self) -> Set["Simulatable"]:
        return set(
            Tesseract(
                self.w_coord + dw,
                self.z_coord + dz,
                self.y_coord + dy,
                self.x_coord + dx,
            )
            for dw in range(-1, 2)
            for dz in range(-1, 2)
            for dy in range(-1, 2)
            for dx in range(-1, 2)
            if not dw == dz == dy == dx == 0
        )

    def active(self, previous_state: Set["Simulatable"]) -> bool:
        active_neighbours = sum(
            1 for neighbour in self.adjacent if neighbour in previous_state
        )
        if self in previous_state:
            return active_neighbours in (2, 3)
        return active_neighbours == 3


Simulatable = Union[Cube, Tesseract]


def read_state(text: str, dimensions: int = 3) -> Set[Simulatable]:
    def make_element(y_coord: int, x_coord: int) -> Simulatable:
        if dimensions == 4:
            return Tesseract(0, 0, y_coord, x_coord)
        return Cube(0, y_coord, x_coord)

    return set(
        make_element(y, x)
        for y, line in enumerate(text.split("\n"))
        for x, char in enumerate(line)
        if char == "#"
    )


def relevant_cubes(state: Set[Simulatable]) -> Set[Simulatable]:
    return set(reduce(union, (cube.adjacent for cube in state)))


def cycle(state: Set[Simulatable]) -> Set[Simulatable]:
    return set(filter(lambda c: c.active(state), relevant_cubes(state)))


def cycles(state: Set[Simulatable], quantity: int = 1) -> Set[Simulatable]:
    for _ in range(quantity):
        state = cycle(state)
    return state


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2020, day=17)

    initial = read_state(data)
    print(f"Part 1: {len(cycles(initial, 6))}")

    initial_4d = read_state(data, dimensions=4)
    print(f"Part 2: {len(cycles(initial_4d, 6))}")


if __name__ == "__main__":
    main()
