"""
2017 Day 21
https://adventofcode.com/2017/day/21
"""

from typing import Dict, Tuple
import numpy as np
import aocd  # type: ignore


def array_from_graphic(graphic: str) -> np.ndarray:
    return np.array(
        [[1 if char == "#" else 0 for char in line] for line in graphic.split("/")]
    )


class Rulebook:
    def __init__(self) -> None:
        self.rules: Dict[Tuple[int, ...], np.ndarray] = {}

    @staticmethod
    def tuplify(nparray: np.ndarray) -> Tuple[int, ...]:
        return tuple(nparray.flatten())

    def add_rule(self, pattern: np.ndarray, result: np.ndarray) -> None:
        self.rules[self.tuplify(pattern)] = result

    def add_rule_from_input(self, line: str) -> None:
        pattern, result = tuple(
            array_from_graphic(graphic) for graphic in line.split(" => ")
        )
        for rotations in range(4):
            rotated = np.rot90(pattern, rotations)
            self.add_rule(rotated, result)
            flipped = np.fliplr(rotated)
            self.add_rule(flipped, result)

    def add_rules_from_input(self, text: str) -> None:
        for line in text.split("\n"):
            self.add_rule_from_input(line)

    def enhance_segment(self, segment: np.ndarray) -> np.ndarray:
        return self.rules[self.tuplify(segment)]

    def enhance_row(self, row: int, segments: int) -> np.ndarray:
        return np.hstack(
            [self.enhance_segment(segment) for segment in np.hsplit(row, segments)]
        )

    def enhance_image(self, image: np.ndarray) -> np.ndarray:
        segment_size = 2 if (image.shape[0] % 2 == 0) else 3
        segments = image.shape[0] // segment_size
        return np.vstack(
            [self.enhance_row(row, segments) for row in np.vsplit(image, segments)]
        )


def enhance_x_times(
    image: np.ndarray, rulebook: Rulebook, iterations: int
) -> np.ndarray:
    for _ in range(iterations):
        image = rulebook.enhance_image(image)
    return image


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2017, day=21)

    rulebook = Rulebook()
    rulebook.add_rules_from_input(data)
    image = array_from_graphic(".#./..#/###")

    five = enhance_x_times(image, rulebook, 5)
    print(f"Part 1: {five.sum()}")

    eighteen = enhance_x_times(five, rulebook, 18 - 5)
    print(f"Part 2: {eighteen.sum()}")


if __name__ == "__main__":
    main()
