"""
2022 Day 11
https://adventofcode.com/2022/day/11
"""

from collections import deque
from dataclasses import dataclass
from enum import Enum
from math import prod
import re
import aocd  # type: ignore

RE_MONKEY_ID = re.compile(r"Monkey (\d+)")
RE_STARTING_ITEMS = re.compile(r"  Starting items: ([\d, ]+)")
RE_OPERATION_MUL = re.compile(r"  Operation: new = old \* (\d+)")
RE_OPERATION_ADD = re.compile(r"  Operation: new = old \+ (\d+)")
RE_TEST = re.compile(r"  Test: divisible by (\d+)")
RE_TARGET_TRUE = re.compile(r"    If true: throw to monkey (\d+)")
RE_TARGET_FALSE = re.compile(r"    If false: throw to monkey (\d+)")


class Operation(Enum):
    """
    A mathematical operation carried out when inspecting an item: multiply, add, or square.
    """
    MUL = 0
    ADD = 1
    POW = 2

    def __call__(self, first: int, second: int) -> int:
        if self == Operation.MUL:
            return first * second
        if self == Operation.ADD:
            return first + second
        if self == Operation.POW:
            return int(pow(first, second))
        raise ValueError


@dataclass(frozen=True)
class Monkey:
    """
    A single monkey in the simulation, containing all of its data. Immutable.
    """

    monkey_id: int
    starting_items: tuple[int, ...]
    operation: Operation
    operand: int
    test: int
    target_true: int
    target_false: int

    @classmethod
    def from_description(cls, desc: str) -> "Monkey":
        """
        Read a single monkey from a section of the puzzle input.
        """
        monkey_id = operand = target_true = target_false = 0
        starting_items = None
        operation = Operation.ADD
        test = 1

        for line in desc.split("\n"):
            if match := RE_MONKEY_ID.match(line):
                monkey_id = int(match.groups()[0])
            elif match := RE_STARTING_ITEMS.match(line):
                starting_items = tuple(
                    int(item) for item in match.groups()[0].split(", ")
                )
            elif line == "  Operation: new = old * old":
                operation = Operation.POW
                operand = 2
            elif match := RE_OPERATION_MUL.match(line):
                operation = Operation.MUL
                operand = int(match.groups()[0])
            elif match := RE_OPERATION_ADD.match(line):
                operation = Operation.ADD
                operand = int(match.groups()[0])
            elif match := RE_TEST.match(line):
                test = int(match.groups()[0])
            elif match := RE_TARGET_TRUE.match(line):
                target_true = int(match.groups()[0])
            elif match := RE_TARGET_FALSE.match(line):
                target_false = int(match.groups()[0])

        return cls(
            monkey_id,
            starting_items or (),
            operation,
            operand,
            test,
            target_true,
            target_false,
        )

    @classmethod
    def all_from_description(cls, text: str) -> dict[int, "Monkey"]:
        """
        Read the puzzle input and return a dictionary mapping monkey ID numbers to their initial
        state.
        """
        return {
            monkey.monkey_id: monkey
            for monkey in (cls.from_description(desc) for desc in text.split("\n\n"))
        }


def monkey_business(monkeys: dict[int, Monkey], part_two: bool = False) -> int:
    """
    Simulate the monkey puzzle and return the product of the two largest inspection-counts amongst
    the monkeys.
    """
    counts = {monkey_id: 0 for monkey_id in monkeys.keys()}
    items = {
        monkey_id: deque(monkey.starting_items) for monkey_id, monkey in monkeys.items()
    }

    modulus = prod(monkey.test for monkey in monkeys.values())
    rounds = 10_000 if part_two else 20

    for _ in range(rounds):
        for monkey_id, monkey in monkeys.items():
            holding = items[monkey_id]
            while holding:
                # choose and inspect next item:
                item = monkey.operation(holding.popleft(), monkey.operand)
                counts[monkey_id] = counts.get(monkey_id, 0) + 1

                # relief or other adjustment to worry values
                if part_two:
                    item %= modulus
                else:
                    item //= 3

                # throw item
                target = (
                    monkey.target_true
                    if item % monkey.test == 0
                    else monkey.target_false
                )
                items[target].append(item)

    ordered_counts = sorted(counts.values(), reverse=True)
    return ordered_counts[0] * ordered_counts[1]


def test_part1() -> None:
    """
    Examples for Part 1.
    """
    assert (
        Monkey.from_description(
            "\n".join(
                (
                    "Monkey 0:",
                    "  Starting items: 79, 98",
                    "  Operation: new = old * 19",
                    "  Test: divisible by 23",
                    "    If true: throw to monkey 2",
                    "    If false: throw to monkey 3",
                )
            )
        )
        == Monkey(0, (79, 98), Operation.MUL, 19, 23, 2, 3)
    )
    monkeys = {
        0: Monkey(0, (79, 98), Operation.MUL, 19, 23, 2, 3),
        1: Monkey(1, (54, 65, 75, 74), Operation.ADD, 6, 19, 2, 0),
        2: Monkey(2, (79, 60, 97), Operation.POW, 2, 13, 1, 3),
        3: Monkey(3, (74,), Operation.ADD, 3, 17, 0, 1),
    }
    assert (
        Monkey.all_from_description(
            "\n".join(
                (
                    "Monkey 0:",
                    "  Starting items: 79, 98",
                    "  Operation: new = old * 19",
                    "  Test: divisible by 23",
                    "    If true: throw to monkey 2",
                    "    If false: throw to monkey 3",
                    "",
                    "Monkey 1:",
                    "  Starting items: 54, 65, 75, 74",
                    "  Operation: new = old + 6",
                    "  Test: divisible by 19",
                    "    If true: throw to monkey 2",
                    "    If false: throw to monkey 0",
                    "",
                    "Monkey 2:",
                    "  Starting items: 79, 60, 97",
                    "  Operation: new = old * old",
                    "  Test: divisible by 13",
                    "    If true: throw to monkey 1",
                    "    If false: throw to monkey 3",
                    "",
                    "Monkey 3:",
                    "  Starting items: 74",
                    "  Operation: new = old + 3",
                    "  Test: divisible by 17",
                    "    If true: throw to monkey 0",
                    "    If false: throw to monkey 1",
                )
            )
        )
        == monkeys
    )
    assert monkey_business(monkeys) == 10_605


def test_part2() -> None:
    """
    Examples for Part 2.
    """
    monkeys = {
        0: Monkey(0, (79, 98), Operation.MUL, 19, 23, 2, 3),
        1: Monkey(1, (54, 65, 75, 74), Operation.ADD, 6, 19, 2, 0),
        2: Monkey(2, (79, 60, 97), Operation.POW, 2, 13, 1, 3),
        3: Monkey(3, (74,), Operation.ADD, 3, 17, 0, 1),
    }
    assert monkey_business(monkeys, True) == 2_713_310_158


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2022, day=11)
    monkeys = Monkey.all_from_description(data)

    print(f"Part 1: {monkey_business(monkeys)}")
    print(f"Part 2: {monkey_business(monkeys, True)}")


if __name__ == "__main__":
    main()
