"""
2020 Day 14
https://adventofcode.com/2020/day/14
"""

import re
from typing import Iterator
import aocd # type: ignore
import numpy as np

def written_value(value: int, mask: str) -> int:
    return int(
        ''.join(
            char if mask[ix] == 'X' else mask[ix]
            for ix, char in enumerate(np.binary_repr(value, 36))
        ),
        2
    )

RE_CHANGEMASK = re.compile(r'mask = ([X10]+)')
RE_WRITE = re.compile(r'mem\[(\d+)\] = (\d+)')

def memory_total_after_program(text: str) -> int:
    memory = {}
    mask = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    for line in text.split('\n'):
        match = RE_CHANGEMASK.search(line)
        if match:
            mask = match.group(1)

        match = RE_WRITE.search(line)
        if match:
            address = int(match.group(1))
            value = written_value(int(match.group(2)), mask)
            memory[address] = value

    return sum(memory.values())

def all_memory_addresses(original: str, mask: str) -> Iterator[str]:
    if len(original) == 0:
        yield ''
        return

    for address in all_memory_addresses(original[1:], mask[1:]):
        if mask[0] == '0':
            yield original[0] + address
        if mask[0] == 'X':
            yield '0' + address
        if mask[0] in ('X', '1'):
            yield '1' + address

def memory_total_after_part2_program(text: str) -> int:
    memory = {}
    mask = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    for line in text.split('\n'):
        match = RE_CHANGEMASK.search(line)
        if match:
            mask = match.group(1)

        match = RE_WRITE.search(line)
        if match:
            original = np.binary_repr(int(match.group(1)), 36)
            value = int(match.group(2))
            for address in all_memory_addresses(original, mask):
                memory[address] = value

    return sum(memory.values())

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2020, day=14)

    print(f'Part 1: {memory_total_after_program(data)}')
    print(f'Part 2: {memory_total_after_part2_program(data)}')

if __name__ == '__main__':
    main()
