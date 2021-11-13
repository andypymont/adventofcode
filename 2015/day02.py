"""
2015 Day 2
https://adventofcode.com/2015/day/2
"""

from math import prod
import aocd # type: ignore

def wrap_needed(present: str) -> int:
    """
    Calculate how many square feet of wrapping paper are needed for a present: the total surface
    area plus the area of the smallest size.
    """
    length, width, height = [int(dimension) for dimension in present.split('x')]
    sides = (length*width, width*height, height*length)
    return (2 * sum(sides)) + min(sides)

def test_part1():
    """
    Examples for Part 1.
    """
    assert wrap_needed('2x3x4') == 58
    assert wrap_needed('1x1x10') == 43

def ribbon_needed(present: str) -> int:
    """
    Calculate how many feet of ribbon are needed for a present: the smallest perimeter of any one
    face, plus the cubic feet of volume of the present.
    """
    dimensions = [int(dimension) for dimension in present.split('x')]
    ribbon_around = 2 * (sum(dimensions) - max(dimensions))
    bow = prod(dimensions)
    return ribbon_around + bow

def test_part2():
    """
    Examples for Part 2.
    """
    assert ribbon_needed('2x3x4') == 34
    assert ribbon_needed('1x1x10') == 14

def main():
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2015, day=2)
    presents = data.split('\n')

    print(f'Part 1: {sum(wrap_needed(present) for present in presents)}')
    print(f'Part 2: {sum(ribbon_needed(present) for present in presents)}')

if __name__ == '__main__':
    main()
