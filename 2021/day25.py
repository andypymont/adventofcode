"""
2021 Day 25
https://adventofcode.com/2021/day/25
"""

import aocd  # type: ignore
import numpy as np


def read_map(text: str) -> np.ndarray:
    return np.array([[".>v".index(char) for char in line] for line in text.split("\n")])


def move(seafloor: np.ndarray, cucumber_type: int) -> np.ndarray:
    newfloor = np.zeros_like(seafloor)

    for y, row in enumerate(seafloor):
        for x, val in enumerate(row):
            if val == cucumber_type:
                ny = (y + 1) % seafloor.shape[0] if cucumber_type == 2 else y
                nx = (x + 1) % seafloor.shape[1] if cucumber_type == 1 else x
                if seafloor[ny, nx] == 0:
                    newfloor[ny, nx] = val
                else:
                    newfloor[y, x] = val
            elif val != 0:
                newfloor[y, x] = val

    return newfloor


def next_state(seafloor: np.ndarray) -> np.ndarray:
    return move(move(seafloor, 1), 2)


def moves_until_still(seafloor: np.ndarray) -> np.ndarray:
    prev = np.zeros_like(seafloor)
    moves = 0
    while not (seafloor == prev).all():
        moves += 1
        prev = seafloor
        seafloor = next_state(seafloor)
    return moves


def test_part1() -> None:
    """
    Examples for Part 1.
    """
    assert (
        read_map(
            "\n".join(
                (
                    "v...>>.vv>",
                    ".vv>>.vv..",
                    ">>.>v>...v",
                    ">>v>>.>.v.",
                    "v>v.vv.v..",
                    ">.>>..v...",
                    ".vv..>.>v.",
                    "v.v..>>v.v",
                    "....v..v.>",
                )
            )
        )
        == np.array(
            [
                [2, 0, 0, 0, 1, 1, 0, 2, 2, 1],
                [0, 2, 2, 1, 1, 0, 2, 2, 0, 0],
                [1, 1, 0, 1, 2, 1, 0, 0, 0, 2],
                [1, 1, 2, 1, 1, 0, 1, 0, 2, 0],
                [2, 1, 2, 0, 2, 2, 0, 2, 0, 0],
                [1, 0, 1, 1, 0, 0, 2, 0, 0, 0],
                [0, 2, 2, 0, 0, 1, 0, 1, 2, 0],
                [2, 0, 2, 0, 0, 1, 1, 2, 0, 2],
                [0, 0, 0, 0, 2, 0, 0, 2, 0, 1],
            ]
        )
    ).all()
    zero = np.array(
        [
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1],
            [2, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 2, 2, 2, 0, 0],
        ]
    )
    one = np.array(
        [
            [0, 0, 2, 2, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 2, 0, 0],
        ]
    )
    two = np.array(
        [
            [0, 0, 0, 0, 2, 1, 0],
            [0, 0, 2, 2, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1],
            [2, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ]
    )
    assert (next_state(zero) == one).all()
    assert (next_state(one) == two).all()
    assert (
        moves_until_still(
            np.array(
                [
                    [2, 0, 0, 0, 1, 1, 0, 2, 2, 1],
                    [0, 2, 2, 1, 1, 0, 2, 2, 0, 0],
                    [1, 1, 0, 1, 2, 1, 0, 0, 0, 2],
                    [1, 1, 2, 1, 1, 0, 1, 0, 2, 0],
                    [2, 1, 2, 0, 2, 2, 0, 2, 0, 0],
                    [1, 0, 1, 1, 0, 0, 2, 0, 0, 0],
                    [0, 2, 2, 0, 0, 1, 0, 1, 2, 0],
                    [2, 0, 2, 0, 0, 1, 1, 2, 0, 2],
                    [0, 0, 0, 0, 2, 0, 0, 2, 0, 1],
                ]
            )
        )
        == 58
    )


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2021, day=25)

    seafloor = read_map(data)
    print(f"Part 1: {moves_until_still(seafloor)}")


if __name__ == "__main__":
    main()
