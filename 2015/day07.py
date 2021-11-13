"""
2015 Day 7
https://adventofcode.com/2015/day/7
"""

from dataclasses import dataclass
from operator import __or__, and_, or_, lshift, rshift
from typing import Callable, Dict, Iterable, Union
import aocd # type: ignore

Input = Union[int, str]

@dataclass
class Wire:
    """
    A single wire in the system, with knowledge of its inputs and the operation it will carry out.
    """
    operator: Callable[[int, int], int]
    first: Input
    second: Input

    def evaluate(self, circuit: 'Circuit') -> int:
        """
        Calculate the value for this wire in the context of the given circuit.
        """
        return self.operator(
            circuit.evaluate(self.first),
            circuit.evaluate(self.second)
        )

    @classmethod
    def from_instruction(cls, instruction: str) -> 'Wire':
        """
        Create a Wire instance from a description such as 'x AND y'
        """
        words = instruction.split()

        if len(words) > 1:
            if words[0] == 'NOT':
                return cls(lambda x, y: ~x & 0xffff, words[1], words[1])
            if words[1] == 'AND':
                return cls(and_, words[0], words[2])
            if words[1] == 'OR':
                return cls(or_, words[0], words[2])
            if words[1] == 'LSHIFT':
                return cls(lshift, words[0], words[2])
            if words[1] == 'RSHIFT':
                return cls(rshift, words[0], words[2])

        return cls(__or__, instruction, instruction)

@dataclass
class Circuit:
    """
    Representation of the circuit, storing both the original instructions and a cache of any values
    already resolved.
    """
    wires: Dict[str, Wire]
    cache: Dict[Input, int]

    def evaluate(self, key: Input) -> int:
        """
        Calculate the value at the given key (wire name), or use the cached value if this wire has
        been calculated previously.
        """
        if key in self.cache:
            return self.cache[key]

        value = 0

        if isinstance(key, int):
            value = key
        elif key.isdigit():
            value = int(key)
        elif key in self.wires:
            value = self.wires[key].evaluate(self)

        self.cache[key] = value
        return value

    @classmethod
    def from_wire_descriptions(cls, descriptions: Iterable[str]) -> 'Circuit':
        """
        Create a new Circuit instance from a list of wire descriptions.
        """
        wires: Dict[str, Wire] = {}
        cache: Dict[Input, int] = {}

        for line in descriptions:
            instruction, target = line.split(' -> ')
            wires[target] = Wire.from_instruction(instruction)

        return cls(wires, cache)

def test_part1():
    """
    Examples for Part 1.
    """
    circuit = Circuit.from_wire_descriptions((
        '123 -> x',
        '456 -> y',
        'x AND y -> d',
        'x OR y -> e',
        'x LSHIFT 2 -> f',
        'y RSHIFT 2 -> g',
        'NOT x -> h',
        'NOT y -> i',
    ))
    for (wire, expected) in (
        ('d', 72),
        ('e', 507),
        ('f', 492),
        ('g', 114),
        ('h', 65412),
        ('i', 65079),
        ('x', 123),
        ('y', 456),
    ):
        assert circuit.evaluate(wire) == expected

def main():
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2015, day=7)
    p1_circuit = Circuit.from_wire_descriptions(data.split('\n'))

    p1_result = p1_circuit.evaluate('a')
    print(f'Part 1: {p1_result}')

    p2_circuit = Circuit.from_wire_descriptions(data.split('\n'))
    p2_circuit.cache = {'b': p1_result}
    p2_result = p2_circuit.evaluate('a')
    print(f'Part 2: {p2_result}')

if __name__ == '__main__':
    main()
