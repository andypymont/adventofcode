"""
2017 Day 15
https://adventofcode.com/2017/day/15
"""

from collections import deque
from typing import Dict, Sequence
import aocd # type: ignore
import regex as re # type: ignore

class Judge:

    def __init__(self, comparisons: int):
        self.comparisons = comparisons
        self.count = 0
        self.queues: Dict[str, deque] = {
            'A': deque(),
            'B': deque(),
        }

    @property
    def completed(self) -> bool:
        return self.comparisons <= 0

    def check(self) -> None:
        while len(self.queues['A']) > 0 and len(self.queues['B']) > 0:
            first = self.queues['A'].popleft()
            second = self.queues['B'].popleft()
            self.comparisons -= 1
            if first == second:
                self.count += 1

    def report(self, source: str, hex_number: str) -> None:
        if not self.completed:
            self.queues.get(source, deque()).append(hex_number)
            self.check()

class Generator:

    def __init__(self, name: str, start_value: int, judge: Judge, filtered_judge: Judge):
        self.name = name
        self.value = start_value
        self.factor = 16807 if name == 'A' else 48271
        self.check = 4 if name == 'A' else 8
        self.judge = judge
        self.filtered_judge = filtered_judge

    @staticmethod
    def hexstart(number: int) -> str:
        return f'{number:{0}16b}'[-16:]

    def run(self) -> None:
        hex_value = self.hexstart(self.value)

        self.judge.report(self.name, hex_value)
        if self.value % self.check == 0:
            self.filtered_judge.report(self.name, hex_value)

        self.value = (self.value * self.factor) % 2147483647

RE_GENERATORS = re.compile(r'Generator (\w) starts with (\d+)')
def read_start_values(text: str) -> Dict[str, int]:
    return {name: int(val) for name, val in RE_GENERATORS.findall(text)}

def run_full_check(start_values: Dict[str, int]) -> Sequence[int]:
    judges = (
        Judge(40_000_000),
        Judge(5_000_000),
    )
    generators = (
        Generator('A', start_values['A'], *judges),
        Generator('B', start_values['B'], *judges),
    )

    while not all(judge.completed for judge in judges):
        for gen in generators:
            gen.run()

    return tuple(judge.count for judge in judges)

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2017, day=15)
    values = read_start_values(data)

    part1, part2 = run_full_check(values)
    print(f'Part 1: {part1}')
    print(f'Part 2: {part2}')

if __name__ == '__main__':
    main()
