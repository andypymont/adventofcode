"""
2015 Day 5
https://adventofcode.com/2015/day/5
"""

from typing import Callable, Iterable
import regex as re  # type: ignore
import aocd  # type: ignore


def is_nice_word(word: str) -> bool:
    """
    Check if a word is nice by part 1's definition.
    """
    return all(
        (
            re.search(r".*([aeiou].*){3}", word),
            re.search(r"(.)\1", word),
            not re.search(r"(ab|cd|pq|xy)", word),
        )
    )


def count_nice_words(all_words: Iterable[str], checker: Callable[[str], bool]) -> int:
    """
    Count the number of words which are nice, using the given nice-word-checking function.
    """
    return sum(1 for word in all_words if checker(word))


def test_part1():
    """
    Examples for Part 1.
    """
    assert is_nice_word("ugknbfddgicrmopn")
    assert not is_nice_word("jchzalrnumimnmhp")
    assert is_nice_word("aaa")
    assert not is_nice_word("dvszwmarrgswjxmb")
    assert (
        count_nice_words(("ugknbfddgicrmopn", "jchzalrnumimnmhp", "aaa"), is_nice_word)
        == 2
    )


def is_nice_word2(word: str) -> bool:
    """
    Check if a word is nice by part 2's definition.
    """
    return all(
        (
            re.search(r"(..).*\1", word),
            re.search(r"(.).\1", word),
        )
    )


def test_part2():
    """
    Examples for Part 2.
    """
    assert is_nice_word2("qjhvhtzxzqqjkmpb")
    assert is_nice_word2("xxyxx")
    assert not is_nice_word2("uurcxstgmygtbstg")
    assert (
        count_nice_words(("qjhvhtzxzqqjkmpb", "uurcxstgmygtbstg"), is_nice_word2) == 1
    )


def main():
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2015, day=5)
    words = data.split("\n")

    print(f"Part 1: {count_nice_words(words, is_nice_word)}")
    print(f"Part 2: {count_nice_words(words, is_nice_word2)}")


if __name__ == "__main__":
    main()
