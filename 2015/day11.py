"""
2015 Day 11
https://adventofcode.com/2015/day/11
"""

from typing import Sequence
import aocd # type: ignore
import numpy as np

def contains_three_consecutive_letters(password: str) -> bool:
    """
    Return True if the password has at least one occurrence of three consecutive letters, e.g. abc
    or xyz, and False if it has no such ocurrences.
    """
    characters = [ord(char) for char in password]
    return any(
        (a + 1) == b and (b + 1) == c
        for a, b, c in [
            characters[x:x+3] for x in range(len(password) - 2)
        ]
    )

BANNED_CHARS: Sequence[str] = ('i', 'o', 'l')
def contains_banned_characters(password: str) -> bool:
    """
    Return True if the password contains of the banned characters, or False if it does not contain
    any.
    """
    return any(banned in password for banned in BANNED_CHARS)

def contains_two_pairs(password: str) -> bool:
    """
    Return True if the password contains two distinct pairs of matching characters, or False if it
    does not.
    """
    prev = ''
    count_pairs = 0
    for letter in password:
        if letter == prev:
            count_pairs += 1
            prev = ''
        else:
            prev = letter
    return count_pairs >= 2

def is_valid_password(password: str) -> bool:
    """
    Return True if the given password meets all three requirements, or False if it does not meet
    one or more of them.
    """
    return (
        contains_three_consecutive_letters(password)
        and contains_two_pairs(password)
        and not contains_banned_characters(password)
    )

def increment_password(password: str) -> str:
    """
    Return the next candidate for a password following the previous candidate - usable to search
    for possible valid passwords.
    """
    return np.base_repr(int(password, 36) + 1, base=36).lower().replace('0', 'a')

def next_valid_password(password: str) -> str:
    """
    Search for the next password that satisfies the is_valid_password(password) function, following
    on from a previous valid password.
    """
    password = increment_password(password)
    while not is_valid_password(password):
        password = increment_password(password)
    return password

def test_examples():
    """
    Examples from the problem description.
    """
    assert contains_three_consecutive_letters('abc')
    assert not contains_three_consecutive_letters('abd')
    assert not contains_banned_characters('qwerty')
    assert contains_banned_characters('uiop')
    assert contains_two_pairs('aabb')
    assert not contains_two_pairs('aaa')

    assert not is_valid_password('hijklmmn')
    assert not is_valid_password('abbceffg')
    assert not is_valid_password('abbcegjk')
    assert is_valid_password('abcdffaa')
    assert is_valid_password('ghjaabcc')

    assert next_valid_password('abcdefgh') == 'abcdffaa'
    # assert next_valid_password('ghijklmn') == 'ghjaabcc'

def main():
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2015, day=11)

    first = next_valid_password(data)
    print(f'Part 1: {first}')

    second = next_valid_password(first)
    print(f'Part 2: {second}')

if __name__ == '__main__':
    main()
