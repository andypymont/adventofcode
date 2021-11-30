"""
2015 Day 16
https://adventofcode.com/2015/day/16
"""

from dataclasses import dataclass
from operator import __eq__, __gt__, __lt__
from typing import Callable, Dict, Sequence
import regex as re # type: ignore
import aocd # type: ignore

AuntProperties = Dict[str, int]

@dataclass(frozen=True)
class Aunt:
    """
    An Aunt Sue, with her unique number and properties.
    """
    number: int
    properties: AuntProperties

    def matches_profile(self, profile: 'Sequence[Requirement]') -> bool:
        """
        Return a boolean indicating whether this aunt matches the given profile - i.e. all
        properties that she has match the profile, but she isn't required to have them all.
        """
        return all(
            requirement.check_aunt(self) for requirement in profile
        )

    @classmethod
    def from_input_line(cls, line: str) -> 'Aunt':
        """
        Create an aunt from the corresponding line in the puzzle input.
        """
        return cls(
            number=int(re.match(r'Sue (\d+)', line).group(1)),
            properties={prop: int(value) for prop, value in re.findall(r'(\w+): (\d)', line)}
        )

    @classmethod
    def all_from_input(cls, text: str) -> 'Sequence[Aunt]':
        """
        Parse all aunts from the puzzle input.
        """
        return [cls.from_input_line(line) for line in text.split('\n')]

@dataclass
class Requirement:
    """
    A requirement that a prospective Aunt Sue must meet, to be the Sue that we are looking for.
    """
    prop: str
    operator: Callable[[int, int], bool]
    target: int

    def check_aunt(self, aunt: Aunt) -> bool:
        """
        Check an aunt's suitability against this requirement.
        """
        if self.prop not in aunt.properties:
            return True
        return self.operator(aunt.properties[self.prop], self.target)

SIMPLE_PROFILE: Sequence[Requirement] = (
    Requirement('children', __eq__, 3),
    Requirement('cats', __eq__, 7),
    Requirement('samoyeds', __eq__, 2),
    Requirement('pomeranians', __eq__, 3),
    Requirement('akitas', __eq__, 0),
    Requirement('vizslas', __eq__, 0),
    Requirement('goldfish', __eq__, 5),
    Requirement('trees', __eq__, 3),
    Requirement('cars', __eq__, 2),
    Requirement('perfumes', __eq__, 1),
)
COMPLEX_PROFILE: Sequence[Requirement] = (
    Requirement('children', __eq__, 3),
    Requirement('cats', __gt__, 7),
    Requirement('samoyeds', __eq__, 2),
    Requirement('pomeranians', __lt__, 3),
    Requirement('akitas', __eq__, 0),
    Requirement('vizslas', __eq__, 0),
    Requirement('goldfish', __lt__, 5),
    Requirement('trees', __gt__, 3),
    Requirement('cars', __eq__, 2),
    Requirement('perfumes', __eq__, 1),
)

def first_matching_profile(aunts: Sequence[Aunt], profile: Sequence[Requirement]) -> Aunt:
    """
    Find the first aunt that matches the given profile of properties.
    """
    return next(aunt for aunt in aunts if aunt.matches_profile(profile))

def main():
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2015, day=16)
    aunts = Aunt.all_from_input(data)

    print(f'Part 1: {first_matching_profile(aunts, SIMPLE_PROFILE).number}')
    print(f'Part 2: {first_matching_profile(aunts, COMPLEX_PROFILE).number}')

if __name__ == '__main__':
    main()
