"""
2016 Day 15
https://adventofcode.com/2016/day/15
"""

from dataclasses import dataclass
from typing import List
import re
import aocd  # type: ignore


@dataclass(frozen=True)
class Disc:
    """
    A single disc which must be passed to make a successful capsule launch.
    """

    number: int
    positions: int
    initial: int

    def position(self, drop_time: int) -> int:
        """
        Calculate the position of this disc at a given time.
        """
        return (self.initial + drop_time + self.number) % self.positions


re_disc = re.compile(
    r"Disc #(\d+) has (\d+) positions; at time=0, it is at position (\d+)."
)


def read_discs(text: str) -> List[Disc]:
    """
    Read the puzzle input and instantiate Disc objects.
    """
    return [Disc(int(n), int(p), int(i)) for (n, p, i) in re_disc.findall(text)]


def first_successful_time(discs: List[Disc], begin: int = 0) -> int:
    """
    Find the first launch time allow for a successful pass through the discs.
    """
    time = begin
    while not all(disc.position(time) == 0 for disc in discs):
        time += 1
    return time


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2016, day=15)
    all_discs = read_discs(data)

    success = first_successful_time(all_discs)
    print(f"Part 1: {success}")

    all_discs.append(Disc(max(d.number for d in all_discs) + 1, 11, 0))
    print(f"Part 2: {first_successful_time(all_discs, success)}")


if __name__ == "__main__":
    main()
