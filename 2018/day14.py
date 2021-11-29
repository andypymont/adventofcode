"""
2018 Day 14
https://adventofcode.com/2018/day/14
"""

from collections import deque
from itertools import islice
from typing import Dict, Iterator, Tuple
import aocd # type: ignore

def recipe_cache() -> Dict[Tuple[str, str], str]:
    return dict(
        ((str(a), str(b)), str(a + b))
        for a in range(10) for b in range(10)
    )

def recipe_sequence() -> Iterator[str]:
    cache = recipe_cache()
    recipes, elf1, elf2 = '37', 0, 1
    queue = deque(recipes)
    while True:
        while queue:
            yield queue.popleft()
        score = cache[(recipes[elf1], recipes[elf2])]
        queue.extend(score)
        recipes += score
        elf1 = (elf1 + int(recipes[elf1]) + 1) % len(recipes)
        elf2 = (elf2 + int(recipes[elf2]) + 1) % len(recipes)

def ten_scores_following(quantity: int) -> str:
    return ''.join(islice(recipe_sequence(), quantity, quantity+10))

def sequence_appears_after(sequence: str) -> int:
    latest: deque[str] = deque(maxlen=len(sequence))
    for count, recipe in enumerate(recipe_sequence()):
        latest.append(recipe)
        if ''.join(latest) == sequence:
            return 1 + count - len(sequence)
    return -1

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2018, day=14)

    print(f'Part 1: {ten_scores_following(int(data))}')
    print(f'Part 2: {sequence_appears_after(data)}')

if __name__ == '__main__':
    main()
