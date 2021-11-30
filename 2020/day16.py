"""
2020 Day 16
https://adventofcode.com/2020/day/16
"""

import re
from dataclasses import dataclass
from math import prod
from typing import Iterable, Sequence, Tuple
import aocd # type: ignore

@dataclass(frozen=True)
class Rule():
    field: str
    ranges: Tuple[Tuple[int, int], ...]

    @classmethod
    def from_input(cls, field: str, ranges: Iterable[Sequence[str]]) -> 'Rule':
        int_ranges = tuple(
            (int(rg[0]), int(rg[1])) for rg in ranges
        )
        return cls(field, int_ranges)

    def valid_value(self, value: int) -> bool:
        return any(lower <= value <= upper for lower, upper in self.ranges)

RE_RULE = re.compile(r'(.+): (.+)')
RE_RANGES = re.compile(r'(\d+)-(\d+)')
def read_rules(text: str) -> Sequence[Rule]:
    return tuple(
        Rule.from_input(
            field, RE_RANGES.findall(ranges)
        ) for field, ranges in RE_RULE.findall(text)
    )

RE_TICKET = re.compile(r'(\d+)')
def read_my_ticket(text: str) -> Sequence[int]:
    return tuple(map(int, RE_TICKET.findall(text)))

def read_nearby_tickets(text: str) -> Sequence[Sequence[int]]:
    return tuple(tuple(map(int, line.split(','))) for line in text.split('\n')[1:])

def filter_tickets(
    tickets: Sequence[Sequence[int]],
    rules: Sequence[Rule]
) -> Tuple[int, Sequence[Sequence[int]]]:
    invalid_tickets = set()
    error_rate = 0

    for ticket_no, ticket in enumerate(tickets):
        invalid_values = sum(
            value for value in ticket
            if not any(rule.valid_value(value) for rule in rules)
        )
        if invalid_values > 0:
            invalid_tickets.add(ticket_no)
            error_rate += invalid_values

    return (
        error_rate,
        tuple(ticket for ix, ticket in enumerate(tickets) if ix not in invalid_tickets)
    )

def possible_fields(
    tickets: Sequence[Sequence[int]],
    column: int,
    rules: Sequence[Rule]
) -> Sequence[str]:
    values = [ticket[column] for ticket in tickets]
    return tuple(rule.field for rule in rules
                 if all(rule.valid_value(value) for value in values))

def identify_fields(tickets: Sequence[Sequence[int]], rules: Sequence[Rule]) -> Sequence[str]:
    columns = [possible_fields(tickets, column, rules) for column in range(len(tickets[0]))]
    while max(len(possible) for possible in columns) > 1:
        for _, possible in enumerate(columns):
            if len(possible) == 1:
                columns = [
                    tuple(f for f in fields if f != possible[0]) if len(fields) > 1 else fields
                    for fields in columns
                ]
    return tuple(column[0] for column in columns)

def departure_product(ticket: Sequence[int], columns: Sequence[str]) -> int:
    return prod(value for value, column in zip(ticket, columns) if column[:9] == 'departure')

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2020, day=16)

    sections = data.split('\n\n')
    rules = read_rules(sections[0])
    my_ticket = read_my_ticket(sections[1])
    nearby_tickets = read_nearby_tickets(sections[2])

    part1, tickets = filter_tickets(nearby_tickets, rules)
    print(f'Part 1: {part1}')

    fields = identify_fields(tickets, rules)
    part2 = departure_product(my_ticket, fields)
    print(f'Part 2: {part2}')

if __name__ == '__main__':
    main()
