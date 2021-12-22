"""
2018 Day 12
https://adventofcode.com/2018/day/12
"""

from itertools import count
from typing import Dict, Iterable, Set, Tuple
import re
import aocd  # type: ignore

Pattern = Tuple[bool, ...]

RE_INITIAL = re.compile(r"initial state: ([#.]+)")
RE_SPREAD_RULE = re.compile(r"([#.]{5}) => ([#.])")


def read_initial_state(text: str) -> Set[int]:
    match = RE_INITIAL.search(text)
    if match:
        state = match.groups()[0]
        return set(n for n, char in enumerate(state) if char == "#")
    return set()


def read_rule(pattern_str: str, result: str) -> Tuple[Pattern, bool]:
    return (tuple(item == "#" for item in pattern_str), result == "#")


def read_rules(text: str) -> Dict[Pattern, bool]:
    return dict(read_rule(*groups) for groups in RE_SPREAD_RULE.findall(text))


def next_generation(state: Iterable[int], rules: Dict[Pattern, bool]) -> Set[int]:
    return {
        n
        for n in range(min(state) - 2, max(state) + 3)
        if rules.get(tuple(n + delta in state for delta in range(-2, 3)))
    }


def state_pattern(state: Iterable[int]) -> Tuple[int, ...]:
    offset = min(state)
    return tuple(s - offset for s in sorted(state))


def first_repeating_pattern(
    state: Iterable[int], rules: Dict[Pattern, bool]
) -> Dict[str, int]:
    seen: Dict[Tuple[int, ...], Tuple[int, int]] = {}
    for generation in count(1):
        pattern = state_pattern(state)

        first = seen.get(pattern)
        if first:
            return dict(begins=first[0], ends=generation, offset=min(state) - first[1])

        seen[pattern] = (generation, min(state))
        state = next_generation(state, rules)
    return dict(begins=-1, ends=-1, offset=-1)


def run_simulation(
    state: Iterable[int], rules: Dict[Pattern, bool], generations: int
) -> Iterable[int]:
    repeat = first_repeating_pattern(state, rules)

    # advance to the beginning of the repeating cycle (or to the total if it's low enough)
    for _ in range(min(generations, repeat["begins"])):
        state = next_generation(state, rules)
        generations -= 1

    # if the total was low enough, just return now
    if generations == 0:
        return state

    # calculate how many full cycles are needed
    cyclelength = repeat["ends"] - repeat["begins"]
    cycles = generations // cyclelength

    # complete any remainder after the repeated cycles
    for _ in range(generations % cyclelength):
        state = next_generation(state, rules)

    return {x + (cycles * repeat["offset"]) for x in state}


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2018, day=12)
    initial = read_initial_state(data)
    rules = read_rules(data)

    print(f"Part 1: {sum(run_simulation(initial, rules, 20))}")
    print(f"Part 2: {sum(run_simulation(initial, rules, 50_000_000_000))}")


if __name__ == "__main__":
    main()
