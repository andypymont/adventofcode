"""
2016 Day 12
https://adventofcode.com/2016/day/12
"""

from collections import deque
from typing import Callable, Dict, List
import aocd  # type: ignore

Registers = Dict[str, int]


def get(registers: Registers, source: str) -> int:
    """
    Translate a register name or int literal into a value
    """
    if source in registers:
        return registers[source]
    return int(source)


def cpy(registers: Registers, source: str, dest: str) -> None:
    """
    cpy instruction - copy value from source register to dest register
    """
    registers[dest] = get(registers, source)


def inc(registers: Registers, register: str) -> None:
    """
    inc instruction - increment value in given register
    """
    registers[register] += 1


def dec(registers: Registers, register: str) -> None:
    """
    dec instruction - decrement value in given register
    """
    registers[register] -= 1


def add(registers: Registers, source: str, dest: str) -> None:
    """
    add instruction - add value from source register to dest register
    """
    registers[dest] = get(registers, dest) + get(registers, source)


def patched_instructions(instructions: List[List[str]]) -> List[List[str]]:
    """
    Patch the given set of instructions with a faster-running set of replacements to ensure that
    part 2 runs quickly.
    """
    try:
        if all(
            (
                instructions[0][0] == "inc",
                instructions[1][0] == "dec",
                instructions[0][1] != instructions[1][1],
                instructions[2][0] == "jnz",
                instructions[2][1] == instructions[1][1],
                instructions[2][2] == "-2",
            )
        ):
            return [
                ["add", instructions[1][1], instructions[0][1]],
                ["cpy", "0", instructions[1][1]],
                ["jnz", "0", "0"],
            ]

        return []
    except IndexError:
        return []


OPERATIONS: Dict[str, Callable] = dict(cpy=cpy, inc=inc, dec=dec, add=add)


def run_program(text: str, starting_c: int = 0) -> Registers:
    """
    Run the program from the given puzzle input and with the given overrides to starting register
    values.
    """
    registers = dict(a=0, b=0, c=starting_c)
    instructions = [instruction.split() for instruction in text.split("\n")]
    current = 0
    replaced_instructions: deque = deque()

    while current < len(instructions):
        replaced_instructions.extend(
            patched_instructions(instructions[current : current + 3])
        )
        if replaced_instructions:
            cmd, *args = replaced_instructions.popleft()
        else:
            cmd, *args = instructions[current]

        if cmd in OPERATIONS:
            OPERATIONS[cmd](registers, *args)
        elif cmd == "jnz":
            if get(registers, args[0]) != 0:
                current += get(registers, args[1]) - 1

        current += 1

    return registers


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2016, day=12)

    print(f'Part 1: {run_program(data).get("a")}')
    print(f'Part 2: {run_program(data, 1).get("a")}')


if __name__ == "__main__":
    main()
