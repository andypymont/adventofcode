"""
2015 Day 13
https://adventofcode.com/2015/day/13
"""

from itertools import permutations
from typing import Dict, Iterable, Sequence
import aocd # type: ignore

PreferenceTable = Dict[str, Dict[str, int]]
SeatingOrder = Sequence[str]

def read_preferences(text: str) -> PreferenceTable:
    """
    Read the group's preferences from the puzzle input format into a preference table (dict of
    dicts).
    """
    preferences: PreferenceTable = {}
    for line in text.split('\n'):
        words = line[:-1].split()
        person, neighbour, happiness = words[0], words[10], int(words[3])
        happiness = happiness if words[2] == 'gain' else -happiness
        if person not in preferences:
            preferences[person] = {}
        preferences[person][neighbour] = happiness
    return preferences

def individual_happiness(
    preferences: PreferenceTable,
    person: str,
    left_neighbour: str,
    right_neighbour: str) -> int:
    """
    Calculate an individual's happiness given their preferences and proposed neighbours.
    """
    my_preferences = preferences.get(person, {})
    return my_preferences.get(left_neighbour, 0) + my_preferences.get(right_neighbour, 0)

def total_happiness(preferences: PreferenceTable, seating: SeatingOrder) -> int:
    """
    Calculate the total happiness given individuals' preferences and a specific seating order.
    """
    total: int = 0

    for position, person in enumerate(seating):
        left_neighbour = seating[-1] if position == 0 else seating[position-1]
        right_neighbour = seating[(position+1) % len(seating)]
        total += individual_happiness(preferences, person, left_neighbour, right_neighbour)

    return total

def all_possible_seating_orders(preferences: PreferenceTable) -> Iterable[SeatingOrder]:
    """
    Calculate all possible seating orders for all people represented in the given set of
    preferences.
    """
    people = tuple(preferences.keys())
    return permutations(people, len(people))

def best_total_happiness_possible(preferences: PreferenceTable) -> int:
    """
    Calculate the best possible total happiness across the given group.
    """
    return max(
        total_happiness(preferences, seating)
        for seating
        in all_possible_seating_orders(preferences)
    )

def test_example():
    """
    Example from the puzzle description.
    """
    example = '\n'.join((
        'Alice would gain 54 happiness units by sitting next to Bob.',
        'Alice would lose 79 happiness units by sitting next to Carol.',
        'Alice would lose 2 happiness units by sitting next to David.',
        'Bob would gain 83 happiness units by sitting next to Alice.',
        'Bob would lose 7 happiness units by sitting next to Carol.',
        'Bob would lose 63 happiness units by sitting next to David.',
        'Carol would lose 62 happiness units by sitting next to Alice.',
        'Carol would gain 60 happiness units by sitting next to Bob.',
        'Carol would gain 55 happiness units by sitting next to David.',
        'David would gain 46 happiness units by sitting next to Alice.',
        'David would lose 7 happiness units by sitting next to Bob.',
        'David would gain 41 happiness units by sitting next to Carol.',
    ))
    expected = {
        'Alice': {'Bob': 54, 'Carol': -79, 'David': -2},
        'Bob': {'Alice': 83, 'Carol': -7, 'David': -63},
        'Carol': {'Alice': -62, 'Bob': 60, 'David': 55},
        'David': {'Alice': 46, 'Bob': -7, 'Carol': 41},
    }
    assert read_preferences(example) == expected
    assert total_happiness(expected, ('David', 'Alice', 'Bob', 'Carol')) == 330

def main():
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2015, day=13)

    preferences = read_preferences(data)
    print(f'Part 1: {best_total_happiness_possible(preferences)}')

    preferences['me'] = {person: 0 for person in preferences.keys()}
    print(f'Part 2: {best_total_happiness_possible(preferences)}')

if __name__ == '__main__':
    main()
