"""
2021 Day 16
https://adventofcode.com/2021/day/16
"""

from dataclasses import dataclass
from functools import reduce
from operator import add, mul
from typing import Callable, Dict, List, Tuple
import aocd # type: ignore

def decode_char(char: str) -> str:
    number = int(char, 16)
    digits = f'{number:b}'[:4]
    return '0' * (4 - len(digits)) + digits

def decode(text: str) -> str:
    return ''.join(decode_char(char) for char in text)

OPERATIONS: Dict[int, Callable[[int, int], int]] = {
    0: add,
    1: mul,
    2: min,
    3: max,
    5: lambda a, b: 1 if a > b else 0,
    6: lambda a, b: 1 if a < b else 0,
    7: lambda a, b: 1 if a == b else 0,
}

@dataclass(frozen=True)
class Packet:
    version: int
    type_id: int
    value: int
    children: Tuple['Packet', ...]

    @classmethod
    def from_binary(cls, binary: str) -> 'Packet':
        return BinaryDataReader(binary).read_packet()

    @classmethod
    def from_hexadecimal(cls, hexadecimal: str) -> 'Packet':
        return cls.from_binary(decode(hexadecimal))

    def calculate(self) -> int:
        if self.type_id == 4:
            return self.value
        return reduce(OPERATIONS[self.type_id], self.children_values())

    def children_values(self) -> Tuple[int, ...]:
        return tuple(child.calculate() for child in self.children)

    def version_sum(self) -> int:
        return self.version + sum(child.version_sum() for child in self.children)

class BinaryDataReader:

    def __init__(self, text: str):
        self.text = text
        self.pos: int = 0

    def read_digit(self) -> str:
        digit = self.text[self.pos]
        self.pos += 1
        return digit

    def read_digits(self, qty: int) -> str:
        digits = self.text[self.pos:self.pos+qty]
        self.pos += qty
        return digits

    def read_number(self, qty: int) -> int:
        return int(self.read_digits(qty), 2)

    def read_literal(self) -> int:
        final = False
        value = ''
        while not final:
            final = (self.read_digit() == '0')
            value += self.read_digits(4)
        return int(value, 2)

    def read_subpackets_by_length(self, length: int) -> Tuple[Packet, ...]:
        limit = self.pos + length
        packets: List[Packet] = []
        while self.pos < limit:
            packets.append(self.read_packet())
        return tuple(packets)

    def read_subpackets_by_quantity(self, qty: int) -> Tuple[Packet, ...]:
        packets: List[Packet] = []
        while len(packets) < qty:
            packets.append(self.read_packet())
        return tuple(packets)

    def read_packet(self) -> Packet:
        version = self.read_number(3)
        type_id = self.read_number(3)
        children: Tuple[Packet, ...] = ()

        if type_id == 4:
            return Packet(version, type_id, self.read_literal(), children)

        length_type = self.read_digit()
        if length_type == '0': # length type 0 = 15-bit length, length is # of bits
            children = self.read_subpackets_by_length(self.read_number(15))
        else: # length type 1 = 11-bit length, length is # of sub-packets
            children = self.read_subpackets_by_quantity(self.read_number(11))
        return Packet(version, type_id, 0, children)

def test_part1() -> None:
    """
    Examples for Part 1.
    """
    assert decode('C') == '1100'
    assert decode('3') == '0011'
    assert decode('A9') == '10101001'
    assert decode('01') == '00000001'
    assert decode('D2FE28') == '110100101111111000101000'
    assert Packet.from_binary('110100101111111000101000') == Packet(6, 4, 2021, tuple())
    assert Packet.from_binary(
        '00111000000000000110111101000101001010010001001000000000'
    ) == Packet(1, 6, 0, (Packet(6, 4, 10, ()), Packet(2, 4, 20, ())))
    assert Packet.from_binary(
        '11101110000000001101010000001100100000100011000001100000'
    ) == Packet(7, 3, 0, (Packet(2, 4, 1, ()), Packet(4, 4, 2, ()), Packet(1, 4, 3, ())))
    assert Packet.from_hexadecimal('8A004A801A8002F478').version_sum() == 16
    assert Packet.from_hexadecimal('620080001611562C8802118E34').version_sum() == 12
    assert Packet.from_hexadecimal('C0015000016115A2E0802F182340').version_sum() == 23
    assert Packet.from_hexadecimal('A0016C880162017C3686B18A3D4780').version_sum() == 31

def test_part2() -> None:
    """
    Examples for Part 2.
    """
    assert Packet.from_hexadecimal('C200B40A82').calculate() == 3
    assert Packet.from_hexadecimal('04005AC33890').calculate() == 54
    assert Packet.from_hexadecimal('880086C3E88112').calculate() == 7
    assert Packet.from_hexadecimal('CE00C43D881120').calculate() == 9
    assert Packet.from_hexadecimal('D8005AC2A8F0').calculate() == 1
    assert Packet.from_hexadecimal('F600BC2D8F').calculate() == 0
    assert Packet.from_hexadecimal('9C005AC2F8F0').calculate() == 0
    assert Packet.from_hexadecimal('9C0141080250320F1802104A08').calculate() == 1

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2021, day=16)
    packets = Packet.from_hexadecimal(data)

    print(f'Part 1: {packets.version_sum()}')
    print(f'Part 2: {packets.calculate()}')

if __name__ == '__main__':
    main()
