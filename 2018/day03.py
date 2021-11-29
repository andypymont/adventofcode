"""
2018 Day 3
https://adventofcode.com/2018/day/3
"""

from dataclasses import dataclass
from typing import Sequence
import re
import numpy as np
import aocd # type: ignore

RE_CLAIM = re.compile(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)')

@dataclass(frozen=True)
class Claim():
    number: int
    left: int
    top: int
    width: int
    height: int

    @property
    def bottom(self) -> int:
        return self.top + self.height

    @property
    def right(self) -> int:
        return self.left + self.width

    def overlaps(self, claimgrid: np.ndarray) -> int:
        window = claimgrid[self.top:self.bottom,self.left:self.right]
        return sum(1 for item in window.flatten() if item > 1)

    @classmethod
    def from_regex_groups(cls, groups: Sequence[str]) -> 'Claim':
        return cls(*map(int, groups))

    @classmethod
    def all_from_text(cls, text: str) -> Sequence['Claim']:
        return [cls.from_regex_groups(groups) for groups in RE_CLAIM.findall(text)]

def claim_grid(claims: Sequence[Claim]) -> np.ndarray:
    width = max(claim.right for claim in claims)
    height = max(claim.bottom for claim in claims)
    grid = np.zeros((width, height), 'int', order='C')
    for claim in claims:
        grid[claim.top:claim.bottom,claim.left:claim.right] += 1
    return grid

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2018, day=3)

    claims = Claim.all_from_text(data)
    grid = claim_grid(claims)

    print(f'Part 1: {sum(1 for item in grid.flatten() if item > 1)}')
    print(f'Part 2: {next(claim.number for claim in claims if claim.overlaps(grid) == 0)}')

if __name__ == '__main__':
    main()
