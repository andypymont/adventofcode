"""
2021 Day 7
https://adventofcode.com/2021/day/7
"""

from typing import Iterable, Tuple
import aocd # type: ignore

def read_crabs(text: str) -> Tuple[int, ...]:
    return tuple(int(x) for x in text.split(','))

def fuel_for_distance(dist: int) -> int:
    return sum(range(dist+1))

def fuel_needed(crabs: Iterable[int], new_pos: int, non_constant: bool = False) -> int:
    fuel = fuel_for_distance if non_constant else lambda f: f
    return sum(fuel(abs(crab_pos - new_pos)) for crab_pos in crabs)

def lowest_fuel_needed(crabs: Iterable[int], non_constant: bool = False) -> int:
    lowest, highest = min(crabs), max(crabs)
    needed = {pos: fuel_needed(crabs, pos, non_constant) for pos in range(lowest, highest+1)}
    return min(needed.values())

def test_part1() -> None:
    """
    Examples for Part 1.
    """
    crabs = (16, 1, 2, 0, 4, 2, 7, 1, 2, 14)
    assert read_crabs('16,1,2,0,4,2,7,1,2,14') == crabs
    assert fuel_needed(crabs, 2) == 37
    assert fuel_needed(crabs, 1) == 41
    assert fuel_needed(crabs, 3) == 39
    assert fuel_needed(crabs, 10) == 71
    assert lowest_fuel_needed(crabs) == 37

def test_part2() -> None:
    """
    Examples for Part 2.
    """
    crabs = (16, 1, 2, 0, 4, 2, 7, 1, 2, 14)
    assert fuel_needed(crabs, 2, True) == 206
    assert fuel_needed(crabs, 5, True) == 168
    assert lowest_fuel_needed(crabs, True) == 168

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2021, day=7)
    crabs = read_crabs(data)

    print(f'Part 1: {lowest_fuel_needed(crabs)}')
    print(f'Part 2: {lowest_fuel_needed(crabs, True)}')

if __name__ == '__main__':
    main()
