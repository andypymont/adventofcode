"""
2021 Day 18
https://adventofcode.com/2021/day/18
"""

import json
import string
from collections import deque
from functools import reduce
from itertools import permutations
from typing import Iterable, Iterator, Tuple
import aocd # type: ignore

def brackets(text: str) -> Iterator[Tuple[int, int, int]]:
    starts: deque[int] = deque()
    depth = 0
    for pos, char in enumerate(text):
        if char == '[':
            depth += 1
            starts.append(pos)
        elif char == ']':
            yield depth, starts.pop()+1, pos
            depth -= 1

def literals(text: str) -> Iterator[Tuple[int, int]]:
    start = -1
    for pos, char in enumerate(text):
        if char in string.digits and start == -1:
            start = pos
        if char not in string.digits:
            if start != -1:
                yield start, pos
            start = -1

def explode(text: str) -> str:
    five_deep = [b for b in brackets(text) if b[0] == 5]
    if not five_deep:
        return text

    _, start, finish = five_deep[0]
    left_add, right_add = [int(half) for half in text[start:finish].split(',')]

    lits = tuple(literals(text))
    try:
        left_start, left_end = next(lit for lit in reversed(lits) if lit[1] < start)
        left_val = int(text[left_start:left_end]) + left_add
        left = f'{text[:left_start]}{left_val}{text[left_end:start-1]}0'
    except StopIteration:
        left = text[:start-1] + '0'
    try:
        right_start, right_end = next(lit for lit in lits if lit[0] > finish)
        right_val = int(text[right_start:right_end]) + right_add
        right = f'{text[finish+1:right_start]}{right_val}{text[right_end:]}'
    except StopIteration:
        right = text[finish+1:]

    return left+right

def split_value(value_str: str) -> str:
    value = int(value_str)
    return f'[{value//2},{value-(value//2)}]'

def split(text: str) -> str:
    try:
        start, finish = next(
            lit for lit in literals(text) if int(text[lit[0]:lit[1]]) > 9
        )
        return f'{text[:start]}{split_value(text[start:finish])}{text[finish:]}'
    except StopIteration:
        return text

def reduce_snailfish(snailfish: str) -> str:
    while True:
        prev, snailfish = snailfish, explode(snailfish)
        if snailfish == prev:
            prev, snailfish = snailfish, split(snailfish)
            if snailfish == prev:
                return snailfish

def add_snailfish(first: str, second: str) -> str:
    return reduce_snailfish(f'[{first},{second}]')

def calc_magnitude(item: object) -> int:
    if isinstance(item, int):
        return item
    if isinstance(item, list):
        return (3 * calc_magnitude(item[0])) + (2 * calc_magnitude(item[1]))
    raise NotImplementedError

def magnitude(number: str) -> int:
    return calc_magnitude(json.loads(number))

def highest_magnitude_sum(numbers: Iterable[str]) -> int:
    combined = {add_snailfish(first, second) for first, second in permutations(numbers, 2)}
    return max(magnitude(combo) for combo in combined)

def test_part1() -> None:
    """
    Examples for Part 1.
    """
    assert add_snailfish('[1,2]', '[[3,4],5]') == '[[1,2],[[3,4],5]]'
    assert explode('[1,2]') == '[1,2]'
    assert explode('[[[[[9,8],1],2],3],4]') == '[[[[0,9],2],3],4]'
    assert explode('[7,[6,[5,[4,[3,2]]]]]') == '[7,[6,[5,[7,0]]]]'
    assert explode('[[6,[5,[4,[3,2]]]],1]') == '[[6,[5,[7,0]]],3]'
    assert explode('[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]') == '[[[[0,7],4],[7,[[8,4],9]]],[1,1]]'
    assert split('[7,[6,[5,[4,[3,2]]]]]') == '[7,[6,[5,[4,[3,2]]]]]'
    assert split('[[[[0,7],4],[15,[0,13]]],[1,1]]') == '[[[[0,7],4],[[7,8],[0,13]]],[1,1]]'
    assert split('[[[[0,7],4],[[7,8],[0,13]]],[1,1]]') == '[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]'
    assert reduce_snailfish(
        '[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]'
    ) == '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]'
    assert add_snailfish(
        '[[[[4,3],4],4],[7,[[8,4],9]]]', '[1,1]'
    ) == '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]'
    assert reduce(
        add_snailfish,
        ['[1,1]', '[2,2]', '[3,3]', '[4,4]', '[5,5]', '[6,6]']
    ) == '[[[[5,0],[7,4]],[5,5]],[6,6]]'
    assert reduce(
        add_snailfish,
        [
        '[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]',
        '[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]',
        '[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]',
        '[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]',
        '[7,[5,[[3,8],[1,4]]]]',
        '[[2,[2,2]],[8,[8,1]]]',
        '[2,9]',
        '[1,[[[9,3],9],[[9,0],[0,7]]]]',
        '[[[5,[7,4]],7],1]',
        '[[[[4,2],2],6],[8,7]]',
    ]
    ) == '[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]'
    assert magnitude('[9,1]') == 29
    assert magnitude('[[[[3,0],[5,3]],[4,4]],[5,5]]') == 791
    assert magnitude('[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]') == 3488

def test_part2() -> None:
    """
    Examples for Part 2.
    """
    examples = [
        '[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]',
        '[[[5,[2,8]],4],[5,[[9,9],0]]]',
        '[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]',
        '[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]',
        '[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]',
        '[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]',
        '[[[[5,4],[7,7]],8],[[8,3],8]]',
        '[[9,3],[[9,9],[6,[4,9]]]]',
        '[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]',
        '[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]',
    ]
    assert highest_magnitude_sum(examples) == 3993

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2021, day=18)
    numbers = data.split('\n')

    total = reduce(add_snailfish, numbers)
    print(f'Part 1: {magnitude(total)}')

    print(f'Part 2: {highest_magnitude_sum(numbers)}')

if __name__ == '__main__':
    main()
