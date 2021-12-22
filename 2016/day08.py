"""
2016 Day 8
https://adventofcode.com/2016/day/8
"""

from typing import Callable, Sequence, Tuple
import re
import numpy as np
import aocd  # type: ignore


def blank_screen() -> np.ndarray:
    """
    Create an empty 50x6 array.
    """
    return np.array([[0 for col in range(50)] for row in range(6)], int)


def rotate_row(screen: np.ndarray, target_row: int, distance: int) -> np.ndarray:
    """
    Rotate a specific row by a number of steps, with any items falling off the end being returned
    to the opposite side.
    """
    return np.array(
        [
            np.roll(row, distance) if r == target_row else row
            for r, row in enumerate(screen)
        ]
    )


def rotate_col(screen: np.ndarray, target_col: int, distance: int) -> np.ndarray:
    """
    Rotate a specific column by a number of steps, with any items falling off the end being
    returned to the oppoisite side.
    """
    rotated = np.rot90(screen, axes=(1, 0))
    rolled = rotate_row(rotated, target_col, -distance)
    return np.rot90(rolled, axes=(0, 1))


def rect(screen: np.ndarray, width: int, height: int) -> np.ndarray:
    """
    Return a modified version of the screen with the values in a 'width' x 'height' rectangle at
    the top left being set to 1.
    """
    return np.array(
        [
            [1 if c < width and r < height else val for (c, val) in enumerate(row)]
            for (r, row) in enumerate(screen)
        ]
    )


ScreenFunction = Callable[[np.ndarray, int, int], np.ndarray]
Operation = Tuple[re.Pattern, ScreenFunction]

OPERATIONS: Sequence[Operation] = [
    (re.compile(regex), screen_function)
    for (regex, screen_function) in (
        (r"rect (\d+)x(\d+)", rect),
        (r"rotate row y=(\d+) by (\d+)", rotate_row),
        (r"rotate column x=(\d+) by (\d+)", rotate_col),
    )
]


def run(text: str) -> np.ndarray:
    """
    Create a blank screen, run all of the commands in the given text in sequence, and then return
    the resulting 2d array.
    """
    screen = blank_screen()
    for instruction in text.split("\n"):
        for (regex, func) in OPERATIONS:
            search = regex.search(instruction)
            if search:
                screen = func(screen, *[int(arg) for arg in search.groups()])
    return screen


def display(screen: np.ndarray) -> str:
    """
    Create a string representation of the screen.
    """
    return "\n".join(
        "".join("■" if char == 1 else " " for char in line) for line in screen
    )


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2016, day=8)
    screen = run(data)

    print(f"Part 1: {screen.sum()}")
    print(f"Part 2:\n{display(screen)}")


if __name__ == "__main__":
    main()
