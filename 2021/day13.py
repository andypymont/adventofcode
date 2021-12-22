"""
2021 Day 13
https://adventofcode.com/2021/day/13
"""

from typing import Tuple
import aocd  # type: ignore
import numpy as np


def read_point(text: str) -> Tuple[int, int]:
    vals = [int(x) for x in text.split(",")]
    return vals[0], vals[1]


def read_paper(text: str) -> np.ndarray:
    points = {read_point(line) for line in text.split("\n")}
    max_x, max_y = max(pt[0] for pt in points), max(pt[1] for pt in points)
    return np.array(
        [
            [1 if (x, y) in points else 0 for x in range(max_x + 1)]
            for y in range(max_y + 1)
        ]
    )


def read_fold(text: str) -> Tuple[str, int]:
    parts = text.split(" ")[-1].split("=")
    return parts[0], int(parts[1])


def read_folds(text: str) -> Tuple[Tuple[str, int], ...]:
    return tuple(read_fold(line) for line in text.split("\n"))


def fold(paper: np.ndarray, split_on: str, position: int) -> np.ndarray:
    # Split the page vertically or horizontally into two parts:
    part1 = paper[:position] if split_on == "y" else paper[:, :position]
    part2 = paper[position + 1 :] if split_on == "y" else paper[:, position + 1 :]

    # Check if the parts are different sizes and, if so, pad the smaller one with zeros
    if part1.shape != part2.shape:
        top_pad = max(part2.shape[0] - part1.shape[0], 0)
        bottom_pad = max(part1.shape[0] - part2.shape[0], 0)
        left_pad = max(part2.shape[1] - part1.shape[1], 0)
        right_pad = max(part1.shape[1] - part2.shape[1], 0)
        part1 = np.pad(part1, ((top_pad, 0), (left_pad, 0)))
        part2 = np.pad(part2, ((0, bottom_pad), (0, right_pad)))

    # Flip the part being folded (right/lower)
    folded = np.flipud(part2) if split_on == "y" else np.fliplr(part2)

    # Put the pieces together and carry over any dots from either
    return part1 | folded


def print_paper(paper: np.ndarray) -> str:
    return "\n".join("".join("█" if val == 1 else " " for val in row) for row in paper)


def test_part1() -> None:
    """
    Examples for Part 1.
    """
    paper = np.array(
        [
            [0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
    )
    assert (
        read_paper(
            "\n".join(
                (
                    "6,10",
                    "0,14",
                    "9,10",
                    "0,3",
                    "10,4",
                    "4,11",
                    "6,0",
                    "6,12",
                    "4,1",
                    "0,13",
                    "10,12",
                    "3,4",
                    "3,0",
                    "8,4",
                    "1,10",
                    "2,14",
                    "8,10",
                    "9,0",
                )
            )
        )
        == paper
    ).all()
    folds = (("y", 7), ("x", 5))
    assert read_folds("fold along y=7\nfold along x=5") == folds
    fold1 = np.array(
        [
            [1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
    )
    assert (fold(paper, *folds[0]) == fold1).all()
    fold2 = np.array(
        [
            [1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ]
    )
    assert (fold(fold1, *folds[1]) == fold2).all()


def test_part2() -> None:
    """
    Examples for Part 2.
    """
    paper = np.array(
        [
            [1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ]
    )
    printed = "\n".join(
        (
            "█████",
            "█   █",
            "█   █",
            "█   █",
            "█████",
            "     ",
            "     ",
        )
    )
    assert print_paper(paper) == printed


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2021, day=13)
    parts = data.split("\n\n")
    paper = read_paper(parts[0])
    folds = read_folds(parts[1])

    print(f"Part 1: {fold(paper, *folds[0]).sum()}")

    for eachfold in folds:
        paper = fold(paper, *eachfold)
    print(f"Part 2:\n{print_paper(paper)}")


if __name__ == "__main__":
    main()
