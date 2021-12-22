"""
2016 Day 20
https://adventofcode.com/2016/day/20
"""

from typing import Iterator, Sequence, Tuple
import aocd  # type: ignore

Rule = Tuple[int, int]


def read_rule(input_line: str) -> Rule:
    """
    Read the rule contained in the given line of the puzzle input.
    """
    parts = [int(part) for part in input_line.split("-")]
    return (parts[0], parts[1])


def read_rules(text: str) -> Sequence[Rule]:
    """
    Read all the rules from the puzzle input.
    """
    return tuple(sorted(read_rule(line) for line in text.split("\n")))


def valid_ips(rules: Sequence[Rule], maxint: int) -> Iterator[int]:
    """
    Yield all valid IPs from 0 to the provided maximum integer.
    """
    ip_address = 0
    rule = 0
    while ip_address < maxint:
        try:
            lower, upper = rules[rule]
        except IndexError:
            lower, upper = ip_address + 1, ip_address + 1

        if ip_address >= lower:
            if ip_address <= upper:
                ip_address = upper + 1
                continue
            rule += 1
        else:
            yield ip_address
            ip_address += 1


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2016, day=20)
    valid = valid_ips(read_rules(data), 2 ** 32)

    print(f"Part 1: {next(valid)}")
    count_valid = 1 + sum(1 for ip in valid)
    print(f"Part 2: {count_valid}")


if __name__ == "__main__":
    main()
