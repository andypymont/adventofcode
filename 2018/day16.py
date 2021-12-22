"""
2018 Day 16
https://adventofcode.com/2018/day/16
"""

from dataclasses import dataclass
from operator import add, eq, gt, mul, __and__, __or__
from typing import Callable, Dict, List, Tuple
import aocd  # type: ignore
import regex as re  # type: ignore

RE_TUPLE = re.compile(r"(\d+)")
Registers = Tuple[int, ...]


@dataclass
class Operation:
    operator: Callable[[int, int], int]
    immediate: Tuple[bool, bool]

    def operate(self, registers: Registers, args: Registers) -> Registers:
        arg1 = args[1] if self.immediate[0] else registers[args[1]]
        arg2 = args[2] if self.immediate[1] else registers[args[2]]
        return tuple(
            self.operator(arg1, arg2) if i == args[3] else v
            for i, v in enumerate(registers)
        )


first = lambda a, _: a

OPERATIONS = {
    "addr": Operation(add, (False, False)),
    "addi": Operation(add, (False, True)),
    "mulr": Operation(mul, (False, False)),
    "muli": Operation(mul, (False, True)),
    "banr": Operation(__and__, (False, False)),
    "bani": Operation(__and__, (False, True)),
    "borr": Operation(__or__, (False, False)),
    "bori": Operation(__or__, (False, True)),
    "setr": Operation(first, (False, False)),
    "seti": Operation(first, (True, False)),
    "gtir": Operation(gt, (True, False)),
    "gtri": Operation(gt, (False, True)),
    "gtrr": Operation(gt, (False, False)),
    "eqir": Operation(eq, (True, False)),
    "eqri": Operation(eq, (False, True)),
    "eqrr": Operation(eq, (False, False)),
}


@dataclass(frozen=True)
class Sample:
    before: Registers
    inputs: Registers
    after: Registers

    @classmethod
    def from_input_chunk(cls, chunk: str) -> "Sample":
        before, inputs, after = [
            tuple(map(int, RE_TUPLE.findall(line))) for line in chunk.split("\n")
        ]
        return cls(before, inputs, after)

    @classmethod
    def list_from_input(cls, text: str) -> List["Sample"]:
        return [cls.from_input_chunk(chunk) for chunk in text.split("\n\n")]

    def possible_operation(self, operation: Operation) -> bool:
        try:
            return operation.operate(self.before, self.inputs) == self.after
        except IndexError:
            return False

    def possible_operations(self, operations: Dict[str, Operation]) -> int:
        return sum(1 for op in operations.values() if self.possible_operation(op))


def find_opcodes(
    operations: Dict[str, Operation], samples: List[Sample]
) -> Dict[int, Operation]:
    opcodes: Dict[int, str] = {}
    possibilities = {
        sample.inputs[0]: {
            opname for opname, op in operations.items() if sample.possible_operation(op)
        }
        for sample in samples
    }
    while len(opcodes) < len(operations):
        opcodes.update(
            {
                opcode: next(iter(opnames))
                for opcode, opnames in possibilities.items()
                if len(opnames) == 1
            }
        )
        solved = set(opcodes.values())
        for opcode in possibilities:
            possibilities[opcode] = possibilities[opcode] - solved

    return {opcode: operations[opname] for opcode, opname in opcodes.items()}


def run_program(program: str, opcodes: Dict[int, Operation]) -> Registers:
    registers: Registers = (0, 0, 0, 0)
    for line in program.split("\n"):
        args = tuple(map(int, RE_TUPLE.findall(line)))
        registers = opcodes[args[0]].operate(registers, args)
    return registers


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2018, day=16)
    sample_data, program = data.split("\n\n\n\n")
    samples = Sample.list_from_input(sample_data)
    print(
        f"Part 1: {sum(1 for sample in samples if sample.possible_operations(OPERATIONS) >= 3)}"
    )

    opcodes = find_opcodes(OPERATIONS, samples)
    part2, *_ = run_program(program, opcodes)
    print(f"Part 2: {part2}")


if __name__ == "__main__":
    main()
