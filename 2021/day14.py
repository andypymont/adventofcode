"""
2021 Day 14
https://adventofcode.com/2021/day/14
"""

from collections import Counter
from itertools import tee
from typing import Dict, Iterable, Tuple, TypeVar
import aocd # type: ignore

def read_rule(line: str) -> Tuple[str, str]:
    parts = line.split(' -> ')
    if len(parts) != 2:
        raise ValueError
    return parts[0], parts[1]

def read_rules(text: str) -> Dict[str, str]:
    return dict(read_rule(line) for line in text.split('\n'))

T = TypeVar('T')
def pairwise(iterable: Iterable[T]) -> Iterable[Tuple[T, T]]:
    """
    Pairwise backport (this is in the standard library in Python 3.10)
    pairwise('ABCDEFG') --> AB BC CD DE EF FG
    """
    one, two = tee(iterable)
    next(two, None)
    return zip(one, two)

def pairs_in_string(text: str) -> Dict[str, int]:
    return Counter(a + b for a, b in pairwise(text))

def substitute(pairs: Dict[str, int], rules: Dict[str, str]) -> Dict[str, int]:
    new_counts: Dict[str, int] = {}
    for pair, qty in pairs.items():
        if pair in rules:
            new_char = rules[pair]
            left, right = pair[0] + new_char, new_char + pair[1]
            new_counts[left] = new_counts.get(left, 0) + qty
            new_counts[right] = new_counts.get(right, 0) + qty
        else:
            new_counts[pair] = new_counts.get(pair, 0) + qty
    return new_counts

def character_counts(initial: str, rules: Dict[str, str], steps: int) -> Dict[str, int]:
    # Calculate the number of each pair and run the subsitution
    pairs = pairs_in_string(initial)
    for _ in range(steps):
        pairs = substitute(pairs, rules)

    # Count the characters from the pairs
    counts: Dict[str, int] = {}
    for pair, qty in pairs.items():
        counts[pair[0]] = counts.get(pair[0], 0) + qty
        counts[pair[1]] = counts.get(pair[1], 0) + qty

    # Each character is in 2 pairs except the characters on the left and right end initially, so we
    # adjust these accordingly
    counts[initial[0]] += 1
    counts[initial[-1]] += 1
    return {char: paircount//2 for char, paircount in counts.items()}

def test_part1() -> None:
    """
    Examples for Part 1.
    """
    rules = {
        'CH': 'B',
        'HH': 'N',
        'CB': 'H',
        'NH': 'C',
        'HB': 'C',
        'HC': 'B',
        'HN': 'C',
        'NN': 'C',
        'BH': 'H',
        'NC': 'B',
        'NB': 'B',
        'BN': 'B',
        'BB': 'N',
        'BC': 'B',
        'CC': 'N',
        'CN': 'C',
    }
    assert read_rules('\n'.join((
        'CH -> B',
        'HH -> N',
        'CB -> H',
        'NH -> C',
        'HB -> C',
        'HC -> B',
        'HN -> C',
        'NN -> C',
        'BH -> H',
        'NC -> B',
        'NB -> B',
        'BN -> B',
        'BB -> N',
        'BC -> B',
        'CC -> N',
        'CN -> C',
    ))) == rules
    initial = {
        'CB': 1,
        'NC': 1,
        'NN': 1,
    }
    one = {
        'BC': 1,
        'CH': 1,
        'CN': 1,
        'HB': 1,
        'NB': 1,
        'NC': 1,
    }
    two = {
        'BB': 2,
        'BC': 2,
        'BH': 1,
        'CB': 2,
        'CC': 1,
        'CN': 1,
        'HC': 1,
        'NB': 2,
    }
    three = {
        'BB': 4,
        'BC': 3,
        'BH': 1,
        'BN': 2,
        'CC': 1,
        'CH': 2,
        'CN': 2,
        'HB': 3,
        'HH': 1,
        'NB': 4,
        'NC': 1,
    }
    four = {
        'BB': 9,
        'BC': 4,
        'BH': 3,
        'BN': 6,
        'CB': 5,
        'CC': 2,
        'CN': 3,
        'HC': 3,
        'HH': 1,
        'HN': 1,
        'NB': 9,
        'NC': 1,
        'NH': 1,
    }
    assert pairs_in_string('NNCB') == initial
    assert pairs_in_string('NCNBCHB') == one
    assert pairs_in_string('NBCCNBBBCBHCB') == two
    assert pairs_in_string('NBBBCNCCNBBNBNBBCHBHHBCHB') == three
    assert substitute(initial, rules) == one
    assert substitute(one, rules) == two
    assert substitute(two, rules) == three
    assert substitute(three, rules) == four
    assert character_counts('NNCB', rules, 10) == {
        'B': 1749,
        'C': 298,
        'H': 161,
        'N': 865,
    }

def test_part2() -> None:
    """
    Examples for Part 2.
    """
    rules = {
        'CH': 'B',
        'HH': 'N',
        'CB': 'H',
        'NH': 'C',
        'HB': 'C',
        'HC': 'B',
        'HN': 'C',
        'NN': 'C',
        'BH': 'H',
        'NC': 'B',
        'NB': 'B',
        'BN': 'B',
        'BB': 'N',
        'BC': 'B',
        'CC': 'N',
        'CN': 'C',
    }
    forty = character_counts('NNCB', rules, 40)
    assert forty['B'] == 2_192_039_569_602
    assert forty['H'] == 3_849_876_073

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2021, day=14)
    template, rules_text = data.split('\n\n')
    rules = read_rules(rules_text)

    ten = character_counts(template, rules, 10)
    print(f'Part 1: {max(ten.values()) - min(ten.values())}')

    forty = character_counts(template, rules, 40)
    print(f'Part 2: {max(forty.values()) - min(forty.values())}')

if __name__ == '__main__':
    main()
