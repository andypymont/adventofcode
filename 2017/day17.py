"""
2017 Day 17
https://adventofcode.com/2017/day/17
"""

from dataclasses import dataclass
from typing import Optional
import aocd # type: ignore

@dataclass
class Node:

    value: int
    left: 'Node'
    right: 'Node'

    def __init__(self, value: int, left: Optional['Node'] = None, right: Optional['Node'] = None):
        self.value = value
        self.left = left or self
        self.right = right or self

    def insert(self, value: int) -> 'Node':
        new_node = Node(value, self, self.right)
        self.right = new_node
        return new_node

def spinlock(step: int) -> int:
    current = Node(0)
    latest = 0
    while latest < 2017:
        for _ in range(step):
            current = current.right
        latest += 1
        current = current.insert(latest)
    return current.right.value

def value_at_index_one(step: int, times: int) -> int:
    length = 1
    current = 0
    at_one = 0
    for val in range(1, times+1):
        current = (current + step) % length
        length += 1
        current += 1
        if current == 1:
            at_one = val
    return at_one

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2017, day=17)

    step = int(data)
    print(f'Part 1: {spinlock(step)}')
    print(f'Part 2: {value_at_index_one(step, 50_000_000)}')

if __name__ == '__main__':
    main()
