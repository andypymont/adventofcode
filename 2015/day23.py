"""
2015 Day 23
https://adventofcode.com/2015/day/23
"""

from dataclasses import dataclass
from typing import Dict, Sequence, Tuple
import aocd  # type: ignore


@dataclass
class Memory:
    """
    Program memory, containing the register-value mapping and in the instruction pointer.
    """

    registers: Dict[str, int]
    pointer: int

    def get(self, register: str) -> int:
        """
        Return the value in the given register.
        """
        return self.registers.get(register, 0)

    def hlf(self, register: str):
        """
        hlf operation - halve the value in the given register and increment the instruction
        pointer.
        """
        self.registers[register] = self.get(register) // 2
        self.pointer += 1

    def tpl(self, register: str):
        """
        tpl operation - triple the value in the given register and increment the instruction
        pointer.
        """
        self.registers[register] = self.get(register) * 3
        self.pointer += 1

    def inc(self, register: str):
        """
        inc operation - increment the value in the given register and increment the instruction
        pointer.
        """
        self.registers[register] = self.get(register) + 1
        self.pointer += 1

    def jmp(self, offset: int):
        """
        jmp operation - adjust the instruction pointer by the given offset
        """
        self.pointer += offset

    def jie(self, register: str, offset: int):
        """
        jie operation - execute a jmp operation if the given register contains an even value
        """
        if self.get(register) % 2 == 0:
            self.jmp(offset)
        else:
            self.pointer += 1

    def jio(self, register: str, offset: int):
        """
        jio operatin - execute a jmp operation if the given register contains a value of 1
        """
        if self.get(register) == 1:
            self.jmp(offset)
        else:
            self.pointer += 1


ProgramLine = Tuple[str, Sequence[str]]


@dataclass
class Program:
    """
    A program, managing the list of lines from the program input and also its memory state.
    """

    lines: Sequence[ProgramLine]
    memory: Memory

    def __init__(self, text: str, registers: Dict[str, int]):
        self.lines = self.parse_lines_from_input(text)
        self.memory = Memory(registers, 0)

    @staticmethod
    def parse_line_from_input(line: str) -> ProgramLine:
        """
        Read and break down a single line from the puzzle input.
        """
        command = line[:3]
        args = line[4:].split(", ")
        return (command, args)

    @classmethod
    def parse_lines_from_input(cls, text: str) -> Sequence[ProgramLine]:
        """
        Parse all lines from the puzzle input.
        """
        return [cls.parse_line_from_input(line) for line in text.split("\n")]

    @property
    def result(self) -> int:
        """
        Return the program result, i.e. the value in register "b".
        """
        return self.memory.get("b")

    def run(self) -> int:
        """
        Run the program, executing operations until the instruction pointer leaves the program
        space, and then return the result.
        """
        while 0 <= self.memory.pointer < len(self.lines):
            command, args = self.lines[self.memory.pointer]

            if command == "hlf":
                self.memory.hlf(args[0])
            elif command == "tpl":
                self.memory.tpl(args[0])
            elif command == "inc":
                self.memory.inc(args[0])
            elif command == "jmp":
                self.memory.jmp(int(args[0]))
            elif command == "jie":
                self.memory.jie(args[0], int(args[1]))
            elif command == "jio":
                self.memory.jio(args[0], int(args[1]))

        return self.result


def main():
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2015, day=23)

    first = Program(data, {})
    print(f"Part 1: {first.run()}")

    second = Program(data, {"a": 1})
    print(f"Part 1: {second.run()}")


if __name__ == "__main__":
    main()
