"""
2020 Day 5
https://adventofcode.com/2020/day/5
"""

from dataclasses import dataclass
from typing import Sequence
import re
import aocd  # type: ignore

re_seat = re.compile(r"([BF]{7})([LR]{3})")


@dataclass(frozen=True)
class Seat:
    row: int
    col: int

    @property
    def seat_id(self) -> int:
        return (self.row * 8) + self.col

    @classmethod
    def from_regex_groups(cls, groups: Sequence[str]) -> "Seat":
        return cls(
            int(groups[0].replace("F", "0").replace("B", "1"), 2),
            int(groups[1].replace("L", "0").replace("R", "1"), 2),
        )

    @classmethod
    def all_from_text(cls, text: str) -> Sequence["Seat"]:
        return [cls.from_regex_groups(groups) for groups in re_seat.findall(text)]


def find_seat(boarding_passes: Sequence[Seat]) -> int:
    seat_ids = set(bp.seat_id for bp in boarding_passes)
    return next(
        seat
        for seat in range(1024)
        if seat not in seat_ids and seat - 1 in seat_ids and seat + 1 in seat_ids
    )


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2020, day=5)

    boarding_passes = Seat.all_from_text(data)

    print(f"Part 1: {max(bp.seat_id for bp in boarding_passes)}")
    print(f"Part 2: {find_seat(boarding_passes)}")


if __name__ == "__main__":
    main()
