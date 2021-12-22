"""
2016 Day 14
https://adventofcode.com/2016/day/14
"""

from dataclasses import dataclass
from hashlib import md5
from typing import Iterator, List
import re
import aocd  # type: ignore

RE_THREEPEATS = re.compile(r"(\w)\1{2,2}")


def first_threepeat(text: str) -> str:
    """
    Find the first 'threepeated' (i.e. repeated 3 times in a row) character in a string.
    """
    search = RE_THREEPEATS.search(text)
    if search:
        return search.group()[0]
    return ""


def md5hex(text: str) -> str:
    """
    Get the hex digest of the MD5 hash of the given string.
    """
    return md5(text.encode("utf-8")).hexdigest()


def stretched_hash(text: str) -> str:
    """
    Produce the stretched hash of a string by recursively running the MD5 hash algorithm 2017
    times.
    """
    for _ in range(2017):
        text = md5hex(text)
    return text


@dataclass
class KeyCandidate:
    """
    A candidate which could be a key (due to a triple character), but is potentially awaiting the
    examination of the following 1000 hashes.
    """

    hash: str
    char: str
    index: int
    matched: int


def find_keys(
    salt: str, quantity: int, stretched: bool = False
) -> Iterator[KeyCandidate]:
    """
    Search for an appropriate quantity of keys (i.e. exploring candidates with a triple character
    and checking for a hash in the next 1000 in the stream containing five of the character).
    """
    returned = 0
    index = 0
    candidates: List[KeyCandidate] = []
    create_hash = stretched_hash if stretched else md5hex

    while returned < quantity:
        hsh = create_hash(salt + str(index))
        candidates = [
            candidate for candidate in candidates if candidate.index >= (index - 1000)
        ]
        paired = [candidate for candidate in candidates if candidate.char * 5 in hsh]

        if paired:
            for candidate in paired:
                candidate.matched = index

        char = first_threepeat(hsh)
        if char:
            candidates.append(KeyCandidate(hsh, char, index, -1))

        if len(candidates) > 0 and candidates[0].matched > -1:
            candidate, *candidates = candidates
            yield candidate
            returned += 1

        index += 1


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2016, day=14)

    *_, solution1 = find_keys(data, 64)
    print(f"Part 1: {solution1.index}")

    *_, solution2 = find_keys(data, 64, True)
    print(f"Part 2: {solution2.index}")


if __name__ == "__main__":
    main()
