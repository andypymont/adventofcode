"""
2019 Day 2
https://adventofcode.com/2019/day/2
"""

from operator import add, mul
from typing import Callable, Tuple
import aocd  # type: ignore

Program = Tuple[int, ...]


def read_program(text: str) -> Program:
    return tuple(int(value) for value in text.split(","))


def run_program(program: Program) -> Program:
    memory = dict(enumerate(program))
    pointer = 0
    terminated = False
    while not terminated:
        instruction = memory.get(pointer, 99)
        if instruction == 99:
            terminated = True
        else:
            operation: Callable[[int, int], int] = {
                1: add,
                2: mul,
            }[instruction]
            input1 = memory.get(pointer + 1, 0)
            input2 = memory.get(pointer + 2, 0)
            output = memory.get(pointer + 3, 0)
            memory[output] = operation(memory.get(input1, 0), memory.get(input2, 0))
        pointer += 4

    return tuple(memory.get(x, 0) for x in range(max(memory) + 1))


def test_part1() -> None:
    """
    Examples for Part 1.
    """
    assert read_program("1,9,10,3,2,3,11,0,99,30,40,50") == (
        1,
        9,
        10,
        3,
        2,
        3,
        11,
        0,
        99,
        30,
        40,
        50,
    )
    assert run_program((1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50)) == (
        3500,
        9,
        10,
        70,
        2,
        3,
        11,
        0,
        99,
        30,
        40,
        50,
    )
    assert run_program((1, 0, 0, 0, 99)) == (2, 0, 0, 0, 99)
    assert run_program((2, 3, 0, 3, 99)) == (2, 3, 0, 6, 99)
    assert run_program((1, 1, 1, 4, 99, 5, 6, 0, 99)) == (30, 1, 1, 4, 2, 5, 6, 0, 99)


def find_input_values(program: Program, target: int = 19690720) -> Tuple[int, int]:
    for noun, verb in [(a, b) for a in range(100) for b in range(100)]:
        patched = program[0:1] + (noun, verb) + program[3:]
        if run_program(patched)[0] == target:
            return noun, verb
    raise ValueError


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2019, day=2)
    program = read_program(data)

    patched = program[0:1] + (12, 2) + program[3:]
    print(f"Part 1: {run_program(patched)[0]}")

    noun, verb = find_input_values(program)
    print(f"Part 2: {100 * noun + verb}")


if __name__ == "__main__":
    main()
