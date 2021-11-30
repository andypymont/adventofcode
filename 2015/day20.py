"""
2015 Day 20
https://adventofcode.com/2015/day/20
"""

from typing import Dict
import aocd # type: ignore

def deliver(target: int, limit: int = 0, per_drop: int = 10) -> Dict[int, int]:
    """
    Deliver presents to houses, recording how many presents each house receives, and return a
    mapping of house number to total presents.
    """
    houses: Dict[int, int] = {}

    for elf in range(1, target//20):
        for house in range(elf, elf*limit if limit else target//20, elf):
            total = houses.get(house, 0) + (per_drop * elf)
            houses[house] = total
            if total > target:
                break

    return houses

def first_with(delivered: Dict[int, int], target: int):
    """
    Identify the first house to have received the target number of presents.
    """
    return next(
        house
        for house, presents
        in delivered.items()
        if presents >= target
    )

def main():
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2015, day=20)
    target = int(data)

    print(f'Part 1: {first_with(deliver(target), target)}')
    print(f'Part 2: {first_with(deliver(target, limit=50, per_drop=11), target)}')

if __name__ == '__main__':
    main()
