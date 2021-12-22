"""
2017 Day 23
https://adventofcode.com/2017/day/23
"""

from typing import Dict
import aocd  # type: ignore


class Program:
    def __init__(self, text: str):
        self.registers: Dict[str, int] = {}
        self.commands = text.split("\n")
        self.position = 0
        self.mul_count = 0

    def get(self, key: str) -> int:
        try:
            return int(key)
        except ValueError:
            return self.registers.get(key, 0)

    def run_command(self, pos: int) -> None:
        command = self.commands[pos]
        instruction, *args = command.split(" ")
        if instruction == "set":
            self.registers[args[0]] = self.get(args[1])
        elif instruction == "sub":
            self.registers[args[0]] = self.get(args[0]) - self.get(args[1])
        elif instruction == "mul":
            self.registers[args[0]] = self.get(args[0]) * self.get(args[1])
            self.mul_count += 1
        elif instruction == "jnz":
            if self.get(args[0]) != 0:
                self.position += self.get(args[1]) - 1

    def run(self) -> None:
        while self.position < len(self.commands):
            self.run_command(self.position)
            self.position += 1


def prime(number: int) -> bool:
    for factor in range(2, (number // 2) + 1):
        if number % factor == 0:
            return False
    return True


def run_program() -> int:
    return sum(1 for b in range(107900, 124901, 17) if not prime(b))


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2017, day=23)

    program = Program(data)
    program.run()
    print(f"Part 1: {program.mul_count}")

    print(f"Part 2: {run_program()}")


if __name__ == "__main__":
    main()
