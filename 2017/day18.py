"""
2017 Day 18
https://adventofcode.com/2017/day/18
"""

from collections import deque
from operator import add, mul, mod
from typing import Callable, Dict, Optional, Sequence, Union
import aocd  # type: ignore

Value = Union[str, int]
Command = Sequence[Value]

OPERATORS: Dict[Value, Callable[[int, int], int]] = {
    "add": add,
    "mul": mul,
    "mod": mod,
}


def read_value(value: str) -> Union[str, int]:
    try:
        return int(value)
    except ValueError:
        return value


def read_commands(text: str) -> Sequence[Command]:
    return tuple(
        tuple(read_value(v) for v in line.split(" ")) for line in text.split("\n")
    )


class Program:
    def __init__(self, commands: Sequence[Command], prog_no: Optional[int] = None):
        self.commands = commands
        self.position = 0
        self.registers: Dict[Value, int] = {}
        if prog_no is not None:
            self.registers["p"] = prog_no
        self.paused = False
        self.queue: deque[int] = deque()
        self.other_queue: Optional[deque[int]] = None
        self.messages_sent = 0

    @property
    def deadlock(self) -> bool:
        return (self.paused and len(self.queue) == 0) or self.position > len(
            self.commands
        )

    def attach(self, other: "Program") -> None:
        self.other_queue = other.queue
        other.other_queue = self.queue

    def get(self, key: Value) -> int:
        if isinstance(key, int):
            return key
        return self.registers.get(key, 0)

    def step(self) -> None:
        command, *args = self.commands[self.position]
        if command == "snd":
            if self.other_queue is None:
                self.queue.append(self.get(args[0]))
            else:
                self.other_queue.append(self.get(args[0]))
            self.messages_sent += 1
        elif command == "set":
            self.registers[args[0]] = self.get(args[1])
        elif command == "rcv":
            if self.other_queue is None:
                if self.get(args[0]) != 0:
                    self.paused = True
            else:
                if len(self.queue) == 0:
                    self.paused = True
                else:
                    self.registers[args[0]] = self.queue.popleft()
        elif command == "jgz":
            if self.get(args[0]) > 0:
                self.position += self.get(args[1]) - 1
        elif command in ("add", "mul", "mod"):
            operator = OPERATORS[command]
            self.registers[args[0]] = operator(self.get(args[0]), self.get(args[1]))

        self.position += 0 if self.paused else 1

    def run(self) -> None:
        self.paused = False
        while (not self.paused) and self.position < len(self.commands):
            self.step()


def run_duet(commands: Sequence[Command]) -> int:
    prog0 = Program(commands, 0)
    prog1 = Program(commands, 1)
    prog0.attach(prog1)

    while not (prog0.deadlock and prog1.deadlock):
        prog0.run()
        prog1.run()

    return prog1.messages_sent


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2017, day=18)
    commands = read_commands(data)

    prog = Program(commands)
    prog.run()
    print(f"Part 1: {prog.queue.pop()}")

    print(f"Part 2: {run_duet(commands)}")


if __name__ == "__main__":
    main()
