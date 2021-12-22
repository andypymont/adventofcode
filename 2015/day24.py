"""
2015 Day 24
https://adventofcode.com/2015/day/24
"""

from itertools import combinations
from math import prod as qe
from typing import Sequence
import aocd  # type: ignore

ParcelGroup = Sequence[int]


def smallest_first_groups(
    parcels: ParcelGroup, groups: int = 3
) -> Sequence[ParcelGroup]:
    """
    Determine all possible smallest first groups for the given group of parcels.
    """
    group_weight = sum(parcel for parcel in parcels) // groups
    for group_size in range(1, len(parcels)):
        matches = [
            combo
            for combo in combinations(parcels, group_size)
            if sum(combo) == group_weight
        ]
        if matches:
            return matches
    return []


def optimum_loading_entanglement(parcels: ParcelGroup, groups: int = 3) -> int:
    """
    Determine the optimal loading entanglement for the given group of parcels.
    """
    return min(qe(group) for group in smallest_first_groups(parcels, groups))


def main():
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2015, day=24)
    parcels = [int(parcel) for parcel in data.split("\n")]

    print(f"Part 1: {optimum_loading_entanglement(parcels)}")
    print(f"Part 2: {optimum_loading_entanglement(parcels, groups=4)}")


if __name__ == "__main__":
    main()
