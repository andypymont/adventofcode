"""
2017 Day 6
https://adventofcode.com/2017/day/6
"""

from typing import Sequence, Tuple
import aocd # type: ignore

def read_initial_blocks(text: str) -> Sequence[int]:
    return tuple(int(val) for val in text.split('\t'))

def largest_block(blocks: Sequence[int]) -> int:
    largest_size = max(blocks)
    return next(block for block, size in enumerate(blocks) if size == largest_size)

def redistribute_from_largest(blocks: Sequence[int]) -> Sequence[int]:
    blocks = list(blocks)
    source = largest_block(blocks)
    redist = blocks[source]
    blocks[source] = 0
    bank = source + 1
    while redist > 0:
        blocks[bank % len(blocks)] += 1
        redist -= 1
        bank += 1
    return tuple(blocks)

def redistribution_cycles_until_repeat(blocks: Sequence[int]) -> Tuple[int, int]:
    seen = set()

    cycles1 = 0
    while blocks not in seen:
        seen.add(blocks)
        blocks = redistribute_from_largest(blocks)
        cycles1 += 1

    seeking = blocks
    cycles2 = 0
    while (blocks != seeking) or (cycles2 == 0):
        blocks = redistribute_from_largest(blocks)
        cycles2 += 1

    return cycles1, cycles2

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2017, day=6)

    blocks = read_initial_blocks(data)
    part1, part2 = redistribution_cycles_until_repeat(blocks)

    print(f'Part 1: {part1}')
    print(f'Part 2: {part2}')

if __name__ == '__main__':
    main()
