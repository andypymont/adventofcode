"""
2016 Day 3
https://adventofcode.com/2016/day/3
"""

from typing import Iterable, Tuple
import numpy as np
import aocd # type: ignore

Triangle = Tuple[int, int, int]

def read_data(text: str) -> np.ndarray:
    """
    Read data from the puzzle input into a 2d array.
    """
    return np.array([
        [int(value) for value in line.split()] for line in text.split('\n')
    ], int)

def is_valid_triangle(triangle: Triangle) -> bool:
    """
    Return True/False whether this is a valid triangle, i.e. no one side is larger than the other
    two summed.
    """
    side_a, side_b, side_c = triangle
    return (side_a + side_b) > side_c and (side_a + side_c) > side_b and (side_b + side_c) > side_a

def triangles_vertically(triangles: np.ndarray) -> Iterable[Triangle]:
    """
    Rotate the input and construct triangles from each vertical, rather than each horizontal, set
    of 3 numbers.
    """
    rotated = np.rot90(triangles)
    for row in rotated:
        for tri in range(len(row)//3):
            yield row[(tri*3):(tri*3)+3]

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2016, day=3)
    triangles = read_data(data)

    valid_p1 = sum(1 for tri in triangles if is_valid_triangle(tri))
    print(f'Part 1: {valid_p1}')

    valid_p2 = sum(1 for tri in triangles_vertically(triangles) if is_valid_triangle(tri))
    print(f'Part 2: {valid_p2}')

if __name__ == '__main__':
    main()
