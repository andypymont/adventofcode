"""
2015 Day 12
https://adventofcode.com/2015/day/12
"""

import json
from typing import Dict, List, Union
import aocd # type: ignore

JSONObject = Union[Dict, int, List, str]

def sum_all_numbers(item: JSONObject, ignore_red: bool = False) -> int:
    """
    Total all numbers in the given data structure (as parsed from JSON), excluding any containing
    'red' if desired.
    """
    if isinstance(item, int):
        return item

    if isinstance(item, list):
        return sum(sum_all_numbers(child, ignore_red) for child in item)

    if isinstance(item, dict):
        values = tuple(item.values())
        if ignore_red and ('red' in values):
            return 0
        return sum(sum_all_numbers(child, ignore_red) for child in values)

    return 0

def test_examples():
    """
    Examples from the puzzle description.
    """
    assert sum_all_numbers([1, 2, 3]) == 6
    assert sum_all_numbers({'a': 2, 'b': 4}) == 6
    assert sum_all_numbers([[[3]]]) == 3
    assert sum_all_numbers( {"a":{"b":4},"c":-1}) == 3
    assert sum_all_numbers({"a":[-1,1]}) == 0
    assert sum_all_numbers([-1,{"a":1}]) == 0

def main():
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2015, day=12)
    structure = json.loads(data)

    print(f'Part 1: {sum_all_numbers(structure)}')
    print(f'Part 2: {sum_all_numbers(structure, ignore_red=True)}')

if __name__ == '__main__':
    main()
