"""
2017 Day 8
https://adventofcode.com/2017/day/8
"""

from dataclasses import dataclass
from operator import eq, ne, gt, lt, ge, le
from typing import Callable, Dict, Sequence
import aocd  # type: ignore
import regex as re  # type: ignore

Registers = Dict[str, int]

RE_INSTRUCTION = re.compile(r"(\w+) (inc|dec) ([-\d]+) if (\w+) ([!=><]+) ([-\d]+)")

OPS: Dict[str, Callable[[int, int], bool]] = {
    "==": eq,
    "!=": ne,
    ">": gt,
    ">=": ge,
    "<": lt,
    "<=": le,
}


@dataclass(frozen=True)
class Condition:
    register: str
    operation: str
    value: int

    @property
    def operator(self) -> Callable[[int, int], bool]:
        return OPS[self.operation]

    def is_met(self, registers: Registers) -> bool:
        actual = registers.get(self.register, 0)
        return self.operator(actual, self.value)


@dataclass(frozen=True)
class Instruction:
    target: str
    change: int
    condition: Condition

    @classmethod
    def from_regex_groups(cls, groups: Sequence[str]) -> "Instruction":
        reg, incdec, amount, condition_reg, condition_op, condition_val = groups
        condition = Condition(condition_reg, condition_op, int(condition_val))
        change = int(amount) * (1 if incdec == "inc" else -1)
        return cls(reg, change, condition)

    @classmethod
    def all_from_input_text(cls, text: str) -> Sequence["Instruction"]:
        return [
            cls.from_regex_groups(groups) for groups in RE_INSTRUCTION.findall(text)
        ]

    def execute(self, registers: Registers) -> None:
        if self.condition.is_met(registers):
            registers[self.target] = registers.get(self.target, 0) + self.change


def execute_program(text: str) -> Sequence[int]:
    instructions = Instruction.all_from_input_text(text)
    registers: Registers = {}
    maximums = []

    for instruction in instructions:
        instruction.execute(registers)
        maximums.append(max(registers.values()))

    return maximums


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2017, day=8)
    results = execute_program(data)

    print(f"Part 1: {results[-1]}")
    print(f"Part 2: {max(results)}")


if __name__ == "__main__":
    main()
