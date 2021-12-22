"""
2016 Day 10
https://adventofcode.com/2016/day/10
"""

from dataclasses import dataclass
from typing import Dict, List, Sequence, Tuple
import re
import aocd  # type: ignore

re_value = re.compile(r"value (\d+) goes to (\w+) (\d+)")
re_robot = re.compile(r"bot (\d+) gives low to (\w+) (\d+) and high to (\w+) (\d+)")


@dataclass(frozen=True)
class Target:
    """
    Target within the system to deliver numbers to - defined by its genre (bot or output) and its
    reference number.
    """

    genre: str
    number: int


@dataclass
class Robot:
    """
    Robot with knowledge of its two recipients/targets. Will wait until receiving its second number
    and then that dispatch them back to the system environment to deliver to their targets.
    """

    environ: "Environment"
    holding: List[int]
    give_low: Target
    give_high: Target

    def __init__(self, environ: "Environment", match_groups: Sequence[str]):
        low_genre, low_number, high_genre, high_number = match_groups
        self.environ = environ
        self.holding = []
        self.give_low = Target(low_genre, int(low_number))
        self.give_high = Target(high_genre, int(high_number))

    def add(self, value: int) -> None:
        """
        Add a number to the robot - if this is the second deliver, it will in turn dispatch calls
        to envion.deliver(..) with the low and high number held and their respective targets.
        """
        self.holding.append(value)
        if len(self.holding) == 2:
            self.environ.deliver(self.give_low, min(self.holding))
            self.environ.deliver(self.give_high, max(self.holding))


@dataclass
class Environment:
    """
    An interconnected system of robots and outputs.
    """

    robots: Dict[int, Robot]
    outputs: Dict[int, int]

    def __init__(self, instructions: str):
        self.robots = {}
        self.outputs = {}

        for robot_definition in re_robot.findall(instructions):
            bot, args = robot_definition[0], robot_definition[1:]
            self.robots[int(bot)] = Robot(self, args)

        for (initial_value, to_genre, to_number) in re_value.findall(instructions):
            target = Target(to_genre, int(to_number))
            self.deliver(target, int(initial_value))

    def deliver(self, target: Target, value: int) -> None:
        """
        Deliver the given number to its target - either storing it in the outputs of this
        Environment object, or delivering it to the relevant robot via its .add(..) method.
        """
        if target.genre == "bot":
            self.robots[target.number].add(value)
        elif target.genre == "output":
            self.outputs[target.number] = value

    def find_robot_holding(self, search: Tuple[int, int]) -> int:
        """
        Find the ID number of the robot which ends up holding the given pair of values.
        """
        inventory = set(search)
        for number, bot in self.robots.items():
            if set(bot.holding) == inventory:
                return number
        return -1


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2016, day=10)
    env = Environment(data)

    print(f"Part 1: {env.find_robot_holding((61, 17))}")
    print(f"Part 2: {env.outputs[0] * env.outputs[1] * env.outputs[2]}")


if __name__ == "__main__":
    main()
