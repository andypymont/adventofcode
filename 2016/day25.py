"""
2016 Day 25
https://adventofcode.com/2016/day/25
"""

from collections import deque
from itertools import count
from typing import Callable, Dict, Iterator, List, Sequence
import aocd  # type: ignore

Registers = Dict[str, int]


def get(registers: Registers, source: str) -> int:
    if source in registers:
        return registers[source]
    return int(source)


def cpy(registers: Registers, args: Sequence[str]) -> None:
    source, dest, *_ = args
    if dest in registers:
        registers[dest] = get(registers, source)


def inc(registers: Registers, args: Sequence[str]) -> None:
    register = args[0]
    if register in registers:
        registers[register] += 1


def add(registers: Registers, args: Sequence[str]) -> None:
    source, dest, *_ = args
    if dest in registers:
        registers[dest] = get(registers, dest) + get(registers, source)


def dec(registers: Registers, args: Sequence[str]) -> None:
    register = args[0]
    if register in registers:
        registers[register] -= 1


def mul(registers: Registers, args: Sequence[str]) -> None:
    source, dest, *_ = args
    if dest in registers:
        registers[dest] = get(registers, dest) * get(registers, source)


def tgl(instruction: List[str]) -> List[str]:
    cmd, *args = instruction
    if len(args) == 1:
        if cmd == "inc":
            return ["dec", *args]
        return ["inc", *args]
    if len(args) == 2:
        if cmd == "jnz":
            return ["cpy", *args]
        return ["jnz", *args]
    return instruction


def patched_instructions(
    instructions: List[List[str]], current: int
) -> List[List[str]]:
    """
    Patch some of the slower-running parts of the code in the given set of instructions with a
    faster-running set to allow part 2 to execute promptly.
    """
    consider = instructions[current : current + 3]
    if len(consider) == 3:
        if all(
            (
                consider[0][0] == "dec",
                consider[1][0] == "inc",
                len(consider[0]) > 1 and consider[0][1] != consider[1][1],
                consider[2][0] == "jnz",
                len(consider[0]) > 1 and consider[2][1] == consider[0][1],
                len(consider[2]) > 2 and consider[2][2] == "-2",
            )
        ):
            return [
                ["add", consider[0][1], consider[1][1]],
                ["cpy", "0", consider[0][1]],
                ["jnz", "0", "0"],
            ]

    consider = instructions[current : current + 6]
    if len(consider) == 6:
        if all(
            (
                consider[0][0] == "cpy",
                consider[1][0] == "inc",
                consider[2][0] == "dec",
                consider[3][0] == "jnz",
                len(consider[3]) > 2 and consider[3][2] == "-2",
                consider[4][0] == "dec",
                consider[5][0] == "jnz",
                len(consider[5]) > 2 and consider[5][2] == "-5",
            )
        ):
            return [
                ["mul", consider[0][1], consider[4][1]],
                ["add", consider[4][1], consider[1][1]],
                ["cpy", "0", consider[0][2]],
                ["cpy", "0", consider[4][1]],
                ["jnz", "0", "0"],
                ["jnz", "0", "0"],
            ]

    return []


COMMANDS: Dict[str, Callable[[Registers, Sequence[str]], None]] = {
    "cpy": cpy,
    "inc": inc,
    "dec": dec,
    "mul": mul,
    "add": add,
}


def run_program(text: str, initial_a: int) -> Iterator[int]:
    """
    Run the given program, with the given initial value for register 'a' (and an initial value of
    zero for registers 'b', 'c' and 'd'). Return a dictionary mapping register names to values at
    the end of execution.
    """
    registers = dict(a=initial_a, b=0, c=0, d=0)
    instructions = [instruct.split() for instruct in text.split("\n")]
    current = 0
    replaced_instructions: deque[Sequence[str]] = deque()

    while current < len(instructions):
        replaced_instructions.extend(patched_instructions(instructions, current))
        line: Sequence[str] = (
            replaced_instructions.popleft()
            if replaced_instructions
            else instructions[current]
        )
        cmd, *args = line

        if cmd in COMMANDS:
            COMMANDS[cmd](registers, args)
        elif cmd == "jnz":
            if get(registers, args[0]) != 0:
                current += get(registers, args[1]) - 1
        elif cmd == "tgl":
            target = current + get(registers, args[0])
            if 0 <= target < len(instructions):
                instructions[target] = tgl(instructions[target])
        elif cmd == "out":
            yield get(registers, args[0])

        current += 1


def find_starting_a_for_clock_output(text: str) -> int:
    for test in count(1):
        output = run_program(text, test)

        for i in range(10):
            nxt = next(output)
            if nxt != (i % 2):
                break
            if i == 9:
                return test

    return -1


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2016, day=25)
    print(f"Part 1: {find_starting_a_for_clock_output(data)}")


if __name__ == "__main__":
    main()
