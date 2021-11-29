"""
2017 Day 16
https://adventofcode.com/2017/day/16
"""

from string import ascii_lowercase
from typing import Sequence
import aocd # type: ignore

DEFAULT_DANCERS = ascii_lowercase[:16]

def spin(dancers: str, quantity: int) -> str:
    return dancers[-quantity:] + dancers[:-quantity]

def exchange(dancers: str, pos1: int, pos2: int) -> str:
    def new_pos(old_pos: int) -> str:
        if old_pos == pos1:
            return dancers[pos2]
        if old_pos == pos2:
            return dancers[pos1]
        return dancers[old_pos]

    return ''.join(new_pos(pos) for pos in range(len(dancers)))

def partner(dancers: str, dancer1: str, dancer2: str) -> str:
    def new_dancer(old_dancer: str) -> str:
        if old_dancer == dancer1:
            return dancer2
        if old_dancer == dancer2:
            return dancer1
        return old_dancer

    return ''.join(new_dancer(dancer) for dancer in dancers)

def dance_step(step: str, dancers: str) -> str:
    step_type, args = step[0], step[1:]

    if step_type == 's':
        return spin(dancers, int(args))
    if step_type == 'x':
        pos1, pos2 = [int(arg) for arg in args.split('/')]
        return exchange(dancers, pos1, pos2)
    if step_type == 'p':
        dancer1, dancer2 = args.split('/')
        return partner(dancers, dancer1, dancer2)

    raise NotImplementedError(f'Step type {step_type} not implemented')

def dance(steps: Sequence[str], dancers: str = DEFAULT_DANCERS, times: int = 1) -> str:
    for _ in range(times):
        for step in steps:
            dancers = dance_step(step, dancers)
    return dancers

def find_cycle_size(steps: Sequence[str]) -> int:
    initial = ascii_lowercase[:16]
    times = 1
    dancers = dance(steps, initial, 1)
    while dancers != initial:
        dancers = dance(steps, dancers, 1)
        times += 1
    return times

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2017, day=16)
    steps = data.split(',')

    print(f'Part 1: {dance(steps)}')

    cycle_size = find_cycle_size(steps)
    times = 1_000_000 % cycle_size
    print(f'Part 2: {dance(steps, times=times)}')

if __name__ == '__main__':
    main()
