"""
2022 Day D
https://adventofcode.com/2022/day/11
"""

from collections import deque
from dataclasses import dataclass
from enum import Enum
from functools import reduce
from typing import Iterator
import re
import aocd  # type: ignore


class OperationType(Enum):
    """
    A type of numerical operation: multiplication, addition, or raising to the power.
    """

    MULTIPLY = 1
    ADD = 2
    POWER = 3


@dataclass(frozen=True)
class Operation:
    """
    An operation that can be carried out on one of the objects in the simulation.
    """

    op_type: OperationType
    operand: int

    def apply(self, value: int) -> int:
        """
        Apply the operation to a given value and return the result.
        """
        if self.op_type == OperationType.MULTIPLY:
            return value * self.operand
        if self.op_type == OperationType.ADD:
            return value + self.operand
        if self.op_type == OperationType.POWER:
            return int(pow(value, self.operand))
        raise ValueError


RE_MONKEY_ID = re.compile(r"Monkey (\d+)")
RE_STARTING_ITEMS = re.compile(r"  Starting items: ([\d, ]+)")
RE_OPERATION_MUL = re.compile(r"  Operation: new = old \* (\d+)")
RE_OPERATION_ADD = re.compile(r"  Operation: new = old \+ (\d+)")
RE_TEST = re.compile(r"  Test: divisible by (\d+)")
RE_TARGET_TRUE = re.compile(r"    If true: throw to monkey (\d+)")
RE_TARGET_FALSE = re.compile(r"    If false: throw to monkey (\d+)")


@dataclass
class Monkey:
    """
    A single monkey in the simulation, with its carried items, operation and comparison values, and
    throwing targets.
    """

    monkey_id: int
    items: deque[int]
    operation: Operation
    test: int
    target_true: int
    target_false: int
    inspections: int

    @classmethod
    def from_description(cls, desc: str) -> "Monkey":
        """
        Read a single monkey from a section of the puzzle input.
        """
        monkey_id = target_true = target_false = inspections = 0
        items: deque[int] = deque()
        operation = Operation(OperationType.ADD, 0)
        test = 1

        for line in desc.split("\n"):
            if match := RE_MONKEY_ID.match(line):
                monkey_id = int(match.groups()[0])
            elif match := RE_STARTING_ITEMS.match(line):
                for item in match.groups()[0].split(", "):
                    items.append(int(item))
            elif line == "  Operation: new = old * old":
                operation = Operation(OperationType.POWER, 2)
            elif match := RE_OPERATION_MUL.match(line):
                operation = Operation(OperationType.MULTIPLY, int(match.groups()[0]))
            elif match := RE_OPERATION_ADD.match(line):
                operation = Operation(OperationType.ADD, int(match.groups()[0]))
            elif match := RE_TEST.match(line):
                test = int(match.groups()[0])
            elif match := RE_TARGET_TRUE.match(line):
                target_true = int(match.groups()[0])
            elif match := RE_TARGET_FALSE.match(line):
                target_false = int(match.groups()[0])

        return cls(monkey_id, items, operation, test, target_true, target_false, inspections)

    @classmethod
    def all_from_input(cls, text: str) -> dict[int, "Monkey"]:
        """
        Read the puzzle input and return a dictionary mapping monkey ID numbers to their initial
        state.
        """
        return {
            monkey.monkey_id: monkey
            for monkey in [cls.from_description(desc) for desc in text.split("\n\n")]
        }

    def take_turn(self) -> Iterator[tuple[int, int]]:
        """
        Have this monkey take its turn, yielding all thrown items as tuples in the form
        (item, target).
        """
        while self.items:
            # choose and inspect next item:
            item = self.operation.apply(self.items.popleft())
            self.inspections += 1

            # relief:
            item //= 3

            # throw item:
            if item % self.test == 0:
                yield (item, self.target_true)
            else:
                yield (item, self.target_false)


def play_round(monkeys: dict[int, Monkey]) -> dict[int, Monkey]:
    """
    Play a single round of the game, throwing objects between the given monkeys.
    """
    for monkey in monkeys.values():
        for item, target in monkey.take_turn():
            monkeys[target].items.append(item)

    return monkeys


def monkey_business(monkeys: dict[int, Monkey]) -> int:
    """
    Simulate 20 rounds of the game and return the monkey business, i.e. the inspection count of the
    two most active monkeys multiplied together.
    """
    for _ in range(20):
        play_round(monkeys)

    return reduce(
        lambda a, b: int(a * b),
        sorted((monkey.inspections for monkey in monkeys.values()), reverse=True)[:2],
    )


def test_part1() -> None:
    """
    Examples for Part 1.
    """
    assert Operation(OperationType.MULTIPLY, 19).apply(4) == 76
    assert Operation(OperationType.ADD, 6).apply(13) == 19
    assert Operation(OperationType.POWER, 2).apply(4) == 16

    monkeys = {
        0: Monkey(
            0, deque((79, 98)), Operation(OperationType.MULTIPLY, 19), 23, 2, 3, 0
        ),
        1: Monkey(
            1, deque((54, 65, 75, 74)), Operation(OperationType.ADD, 6), 19, 2, 0, 0
        ),
        2: Monkey(
            2, deque((79, 60, 97)), Operation(OperationType.POWER, 2), 13, 1, 3, 0
        ),
        3: Monkey(3, deque((74,)), Operation(OperationType.ADD, 3), 17, 0, 1, 0),
    }

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
        == monkeys[0]
    )
    assert (
        Monkey.all_from_input(
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

    zero = Monkey(
        0, deque((79, 98)), Operation(OperationType.MULTIPLY, 19), 23, 2, 3, 0
    )
    assert tuple(zero.take_turn()) == (
        (500, 3),
        (620, 3),
    )
    assert zero == Monkey(
        0, deque(), Operation(OperationType.MULTIPLY, 19), 23, 2, 3, 2
    )

    one = {
        0: Monkey(
            0, deque((79, 98)), Operation(OperationType.MULTIPLY, 19), 23, 2, 3, 0
        ),
        1: Monkey(
            1, deque((54, 65, 75, 74)), Operation(OperationType.ADD, 6), 19, 2, 0, 0
        ),
        2: Monkey(
            2, deque((79, 60, 97)), Operation(OperationType.POWER, 2), 13, 1, 3, 0
        ),
        3: Monkey(3, deque((74,)), Operation(OperationType.ADD, 3), 17, 0, 1, 0),
    }
    two = {
        0: Monkey(
            0,
            deque((20, 23, 27, 26)),
            Operation(OperationType.MULTIPLY, 19),
            23,
            2,
            3,
            2,
        ),
        1: Monkey(
            1,
            deque((2080, 25, 167, 207, 401, 1046)),
            Operation(OperationType.ADD, 6),
            19,
            2,
            0,
            4,
        ),
        2: Monkey(2, deque(), Operation(OperationType.POWER, 2), 13, 1, 3, 3),
        3: Monkey(3, deque(), Operation(OperationType.ADD, 3), 17, 0, 1, 5),
    }
    assert play_round(one) == two

    assert monkey_business(monkeys) == 10_605


# def test_part2() -> None:
#     """
#     Examples for Part 2.
#     """
#     assert False


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2022, day=11)

    monkeys = Monkey.all_from_input(data)
    print(f"Part 1: {monkey_business(monkeys)}")
    # print(f'Part 2: {p2}')


if __name__ == "__main__":
    main()
