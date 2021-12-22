"""
2019 Day 8
https://adventofcode.com/2019/day/8
"""

from collections import Counter
from functools import reduce
from typing import Dict, Iterable, List
import aocd  # type: ignore
import numpy as np


def read_layer(numbers: Iterable[int], width: int, height: int) -> np.ndarray:
    return np.array(numbers).reshape(height, width)


def read_layers(text: str, width: int = 25, height: int = 6) -> List[np.ndarray]:
    numbers = [int(digit) for digit in text]
    layer_size = width * height
    return [
        read_layer(numbers[x : x + layer_size], width, height)
        for x in range(0, len(numbers), layer_size)
    ]


def layer_counts(layer: np.ndarray) -> Dict[int, int]:
    return Counter(layer.flatten())


def find_relevant_layer_score(layers: Iterable[np.ndarray]) -> int:
    counts = [layer_counts(layer) for layer in layers]
    relevant = min(counts, key=lambda layer: layer[0])
    return relevant[1] * relevant[2]


def stack_layers(top: np.ndarray, bottom: np.ndarray) -> np.ndarray:
    combined = np.array(top)
    height, width = combined.shape
    for row in range(height):
        for col in range(width):
            if top[row, col] == 2:
                combined[row, col] = bottom[row, col]
    return combined


def build_image(layers: Iterable[np.ndarray]) -> np.ndarray:
    return reduce(stack_layers, layers)


def print_image(image: np.ndarray) -> str:
    return "\n".join("".join("#" if val == 1 else " " for val in row) for row in image)


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2019, day=8)
    layers = read_layers(data)

    print(f"Part 1: {find_relevant_layer_score(layers)}")
    print(f"Part 2:\n{print_image(build_image(layers))}")


if __name__ == "__main__":
    main()
