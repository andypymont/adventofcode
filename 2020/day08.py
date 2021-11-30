"""
2020 Day 8
https://adventofcode.com/2020/day/8
"""

import re
from typing import List, Tuple
import aocd # type: ignore

Program = List[Tuple[str, int]]

RE_CODE = re.compile(r'(\w{3}) ([+-]\d+)')
def read_code(text: str) -> Program:
    return [(op, int(val)) for op, val in RE_CODE.findall(text)]

def accumulator_value(code: List[Tuple[str, int]]) -> Tuple[str, int]:
    visited = set()
    pointer = acc = 0
    while pointer < len(code):
        if pointer in visited:
            return ('infinite', acc)
        visited.add(pointer)
        operation, val = code[pointer]
        if operation == 'acc':
            acc += val
        elif operation == 'jmp':
            pointer += val - 1
        pointer += 1
    return ('terminated', acc)

def patched_program(code: Program, pointer: int) -> Program:
    operation, val = code[pointer]
    flipped = 'jmp' if operation == 'nop' else 'nop'
    return code[:pointer] + [(flipped, val)] + code[pointer+1:]

def all_patched_programs(code: Program) -> List[Program]:
    return [patched_program(code, ip) for ip in range(len(code)) if code[ip][0] in ('jmp', 'nop')]

def find_patched_accumulator_value(code: Program) -> int:
    for patched_code in all_patched_programs(code):
        outcome, acc = accumulator_value(patched_code)
        if outcome == 'terminated':
            return acc
    return -1

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2020, day=8)
    code = read_code(data)

    _, part1 = accumulator_value(code)
    print(f'Part 1: {part1}')

    part2 = find_patched_accumulator_value(code)
    print(f'Part 2: {part2}')

if __name__ == '__main__':
    main()
