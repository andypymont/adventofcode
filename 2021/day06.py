"""
2021 Day 6
https://adventofcode.com/2021/day/6
"""

from typing import Dict
import aocd # type: ignore

def read_fish(text: str) -> Dict[int, int]:
    fish = [int(f) for f in text.split(',')]
    return {
        age: sum(1 for f in fish if f == age)
        for age in range(9)
    }

def progress(fish: Dict[int, int], days: int) -> Dict[int, int]:
    for _ in range(days):
        fish = {
            0: fish[1],
            1: fish[2],
            2: fish[3],
            3: fish[4],
            4: fish[5],
            5: fish[6],
            6: fish[7] + fish[0],
            7: fish[8],
            8: fish[0],
        }
    return fish

def fish_count(fish: Dict[int, int], days: int) -> int:
    return sum(progress(fish, days).values())

def test_part1() -> None:
    """
    Examples for Part 1.
    """
    example = {8: 0, 7: 0, 6: 0, 5: 0, 4: 1, 3: 2, 2: 1, 1: 1, 0: 0}
    assert read_fish('3,4,3,1,2') == example
    assert progress(example, 1) == {8: 0, 7: 0, 6: 0, 5: 0, 4: 0, 3: 1, 2: 2, 1: 1, 0: 1}
    assert progress(example, 2) == {8: 1, 7: 0, 6: 1, 5: 0, 4: 0, 3: 0, 2: 1, 1: 2, 0: 1}
    assert progress(example, 18) == {8: 4, 7: 1, 6: 5, 5: 1, 4: 2, 3: 2, 2: 3, 1: 5, 0: 3}
    assert fish_count(example, 18) == 26
    assert fish_count(example, 80) == 5934

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2021, day=6)
    fish = read_fish(data)

    print(f'Part 1: {fish_count(fish, 80)}')
    print(f'Part 2: {fish_count(fish, 256)}')

if __name__ == '__main__':
    main()
