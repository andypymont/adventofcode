"""
2017 Day 5
https://adventofcode.com/2017/day/5
"""

from typing import Callable, List
import aocd  # type: ignore

Jumps = List[int]
ValuePolicyFunction = Callable[[int], int]


def read_jumps(text: str) -> Jumps:
    return [int(x) for x in text.split("\n")]


def increment_by_one(val: int) -> int:
    return val + 1


def varied_based_on_value(val: int) -> int:
    return (val - 1) if (val >= 3) else (val + 1)


def jump(jumps: Jumps, pos: int, new_value_policy: ValuePolicyFunction) -> int:
    new_pos = pos + jumps[pos]
    jumps[pos] = new_value_policy(jumps[pos])
    return new_pos


def steps_until_exit(
    jumps: Jumps, new_value_policy: ValuePolicyFunction = increment_by_one
) -> int:
    pos = 0
    steps = 0
    while 0 <= pos < len(jumps):
        pos = jump(jumps, pos, new_value_policy)
        steps += 1
    return steps


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2017, day=5)

    print(f"Part 1: {steps_until_exit(read_jumps(data))}")
    print(f"Part 2: {steps_until_exit(read_jumps(data), varied_based_on_value)}")


if __name__ == "__main__":
    main()
