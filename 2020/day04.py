"""
2020 Day 4
https://adventofcode.com/2020/day/4
"""

import re
from dataclasses import dataclass
from typing import Optional
import aocd # type: ignore

RE_PASSPORT_FIELDS = re.compile(r'(\w+):(\S+)')
RE_HEIGHT = re.compile(r'(\d+)(cm|in)')
RE_HAIRCOLOR = re.compile(r'(#[\da-f]{6})')

@dataclass(frozen=True)
class Passport():
    byr: Optional[str]
    iyr: Optional[str]
    eyr: Optional[str]
    hgt: Optional[str]
    hcl: Optional[str]
    ecl: Optional[str]
    pid: Optional[str]
    cid: Optional[str]

    @property
    def has_all_required_fields(self) -> bool:
        for required_field in (
            self.byr, self.iyr, self.eyr, self.hgt, self.hcl, self.ecl, self.pid
        ):
            if required_field is None:
                return False
        return True

    @property
    def has_valid_height(self) -> bool:
        if self.hgt:
            height = RE_HEIGHT.search(self.hgt)
            if not height:
                return False
            value, unit = height.groups()
            if unit == 'cm':
                return 150 <= int(value) <= 193
            return 59 <= int(value) <= 76
        return False

    @property
    def is_valid(self) -> bool:
        if not self.has_all_required_fields:
            return False
        return all((
            len(self.byr or '') == 4 and 1920 <= int(self.byr or '0') <= 2002,
            len(self.iyr or '') == 4 and 2010 <= int(self.iyr or '0') <= 2020,
            len(self.eyr or '') == 4 and 2020 <= int(self.eyr or '0') <= 2030,
            self.has_valid_height,
            RE_HAIRCOLOR.search(self.hcl or ''),
            self.ecl and self.ecl in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'),
            self.pid and len(self.pid) == 9 and self.pid.isdigit(),
        ))

    @classmethod
    def from_description(cls, desc: str) -> 'Passport':
        read = dict(RE_PASSPORT_FIELDS.findall(desc))
        return cls(
            read.get('byr'),
            read.get('iyr'),
            read.get('eyr'),
            read.get('hgt'),
            read.get('hcl'),
            read.get('ecl'),
            read.get('pid'),
            read.get('cid'),
        )

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2020, day=4)
    passports = [Passport.from_description(desc) for desc in data.split('\n\n')]

    part1 = sum(1 for passport in passports if passport.has_all_required_fields)
    print(f'Part 1: {part1}')

    part2 = sum(1 for passport in passports if passport.is_valid)
    print(f'Part 2: {part2}')

if __name__ == '__main__':
    main()
