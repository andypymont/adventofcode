"""
2019 Day 4
https://adventofcode.com/2019/day/4
"""

from typing import List, Tuple
import aocd # type: ignore

ASCENDING_PAIRS = {
    '00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '11', '12', '13', '14', '15',
    '16', '17', '18', '19', '22', '23', '24', '25', '26', '27', '28', '29', '33', '34', '35',
    '36', '37', '38', '39', '44', '45', '46', '47', '48', '49', '55', '56', '57', '58', '59',
    '66', '67', '68', '69', '77', '78', '79', '88', '89', '99'
}

def check_password(password: int) -> Tuple[bool, List[str]]:
    passstr = str(password)
    ascending = True
    groups: List[str] = []
    for index, digit in enumerate(passstr):
        prev: str = '' if index == 0 else passstr[index-1]
        if digit == prev:
            groups[len(groups) - 1] += digit
        else:
            groups.append(digit)
        if index > 0:
            pair = passstr[index-1] + digit
            ascending = ascending and (pair in ASCENDING_PAIRS)
    return ascending, groups

def valid_passwords(first: int, last: int) -> Tuple[int, int]:
    checks = [check_password(password) for password in range(first, last+1)]
    groups_by_password = [
        set(len(group) for group in groups)
        for ascending, groups in checks
        if ascending
    ]
    return (
        sum(1 for groups in groups_by_password if max(groups) > 1),
        sum(1 for groups in groups_by_password if 2 in groups)
    )

def test_part1() -> None:
    """
    Examples for Part 1.
    """
    assert check_password(111111) == (True, ['111111'])
    assert check_password(223450) == (False, ['22', '3', '4', '5', '0'])
    assert check_password(123789) == (True, ['1', '2', '3', '7', '8', '9'])

def test_part2() -> None:
    """
    Examples for Part 2.
    """
    assert valid_passwords(555, 566) == (6, 5)

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2019, day=4)
    first, last = [int(value) for value in data.split('-')]

    part1, part2 = valid_passwords(first, last)
    print(f'Part 1: {part1}')
    print(f'Part 2: {part2}')

if __name__ == '__main__':
    main()
