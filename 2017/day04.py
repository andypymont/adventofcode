"""
2017 Day 4
https://adventofcode.com/2017/day/4
"""

from typing import Sequence
import aocd # type: ignore

def sort_word(word: str) -> str:
    return ''.join(char for char in sorted(word))

def valid_passphrase(words: Sequence[str], check_anagrams: bool = False) -> bool:
    seen = set()
    for word in words:
        word = sort_word(word) if check_anagrams else word
        if word in seen:
            return False
        seen.add(word)
    return True

def valid_passphrases(phrases: Sequence[str], check_anagrams: bool = False) -> int:
    return sum(1 for phrase in phrases if valid_passphrase(phrase.split(' '), check_anagrams))

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2017, day=4)
    phrases = data.split('\n')

    print(f'Part 1: {valid_passphrases(phrases)}')
    print(f'Part 2: {valid_passphrases(phrases, True)}')

if __name__ == '__main__':
    main()
