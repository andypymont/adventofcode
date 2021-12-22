"""
2015 Day 25
https://adventofcode.com/2015/day/25
"""

from dataclasses import dataclass
from typing import Iterable
import aocd  # type: ignore
import regex as re  # type: ignore


@dataclass(frozen=True)
class Point:
    """
    Two-dimensional point, which understands the sequence of the code grid.
    """

    x_coord: int
    y_coord: int

    def after(self) -> "Point":
        """
        Calculate the point containing the subsequence code to this point.
        """
        if self.y_coord > 1:
            return self.__class__(self.x_coord + 1, self.y_coord - 1)
        return self.__class__(1, self.x_coord + 1)

    def sequence(self) -> "Iterable[Point]":
        """
        Return the (infinite) sequence of points beginning with this one.
        """
        point = self
        while True:
            yield point
            point = point.after()


def code_number_at_position(target: Point) -> int:
    """
    Return the code number at the given position.
    """
    for number, point in enumerate(Point(0, 0).sequence()):
        if point == target:
            return number + 1
    return -1


def next_value(value: int) -> int:
    """
    Given the current code value, return what the next value will be.
    """
    return (value * 252_533) % 33_554_393


def value_at_position(row: int, col: int) -> int:
    """
    Calculate the value which will be present at the given row and column.
    """
    value = 27_995_004
    iterations = code_number_at_position(Point(col, row)) - 62
    for _ in range(iterations):
        value = next_value(value)
    return value


def main():
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2015, day=25)
    row, col = [int(x) for x in re.findall(r"(\d+)", data)]
    print(f"Part 1: {value_at_position(row, col)}")


if __name__ == "__main__":
    main()
