"""
2016 Day 18
https://adventofcode.com/2016/day/18
"""

from typing import Sequence
import aocd # type: ignore

Line = Sequence[int]

TRAP_COMBOS = {
    (False, False, True),
    (True, False, False),
    (False, True, True),
    (True, True, False),
}
def is_safe(index: int, line: Line) -> bool:
    """
    Return True/False whether the space at the given index of the given line is safe.
    """
    left = True if index == 0 else line[index-1]
    right = True if index+1 == len(line) else line[index+1]
    return (left, line[index], right) not in TRAP_COMBOS

def next_line(current_line: Line) -> Line:
    """
    Calculate the next line from the current line.
    """
    return [is_safe(x, current_line) for x in range(len(current_line))]

def count_safe_spaces(first_line: Line, no_of_lines: int) -> int:
    """
    Return the total quantity of safe spaces in the given number of lines, based on the given first
    line.
    """
    safe = 0
    for _ in range(no_of_lines):
        safe += sum(1 for x in first_line if x)
        first_line = next_line(first_line)
    return safe

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2016, day=18)
    first_line = [char == '.' for char in data]

    print(f'Part 1: {count_safe_spaces(first_line, 40)}')
    print(f'Part 2: {count_safe_spaces(first_line, 400_000)}')

if __name__ == '__main__':
    main()
