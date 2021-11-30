"""
2018 Day 2
https://adventofcode.com/2018/day/2
"""

from collections import Counter
from dataclasses import dataclass
from itertools import combinations
from typing import Sequence
import aocd # type: ignore

@dataclass(frozen=True)
class Box():
    box_id: str

    @property
    def letter_counts(self) -> Counter:
        return Counter(self.box_id)

    def compare(self, other: 'Box') -> str:
        return ''.join(
            letter for (ix, letter) in enumerate(self.box_id)
            if letter == other.box_id[ix]
        )

def checksum(boxes: Sequence[Box]) -> int:
    twos = 0
    threes = 0
    for box in boxes:
        letter_counts = box.letter_counts
        twos += (1 if 2 in letter_counts.values() else 0)
        threes += (1 if 3 in letter_counts.values() else 0)
    return twos * threes

def compare_all_boxes(boxes: Sequence[Box]) -> Sequence[str]:
    return [a.compare(b) for a, b in combinations(boxes, 2)]

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2018, day=2)
    boxes = [Box(box_id) for box_id in data.split('\n')]

    print(f'Part 1: {checksum(boxes)}')

    compared = sorted(compare_all_boxes(boxes), key=len, reverse=True)
    print(f'Part 2: {next(comp for comp in compared)}')

if __name__ == '__main__':
    main()
