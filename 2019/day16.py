"""
2019 Day 16
https://adventofcode.com/2019/day/16
"""

from itertools import cycle, islice
from typing import Iterator, Sequence, Tuple
import aocd  # type: ignore

BASE_PATTERN = (0, 1, 0, -1)


def repeating_pattern(pos: int) -> Iterator[int]:
    for digit in cycle(BASE_PATTERN):
        for _ in range(pos + 1):
            yield digit


def patterns(seq: Sequence[int]) -> Tuple[Tuple[int, ...], ...]:
    length = len(seq)
    return tuple(
        tuple(islice(repeating_pattern(pos), 1, length + 1)) for pos in range(length)
    )


def phase(seq: Sequence[int], patterns: Tuple[Tuple[int, ...], ...]) -> Sequence[int]:
    return tuple(
        abs(sum(dig * pattern_item for dig, pattern_item in zip(seq, pattern))) % 10
        for pattern in patterns
    )


def fft(seq: Sequence[int], phases: int) -> Sequence[int]:
    pats = patterns(seq)
    for _ in range(phases):
        seq = phase(seq, pats)
    return seq


def phase_shortcut(signal: Sequence[int]) -> Sequence[int]:
    sum = 0
    for pos in range(len(signal) - 1, len(signal) // 2, -1):
        sum += signal[pos]
        signal[pos] = sum % 10
    return signal


def fft_real(text: str) -> str:
    offset = int(text[:7])
    signal = [int(digit) for digit in text] * 10_000
    for phase in range(100):
        signal = phase_shortcut(signal)
    return "".join(str(dig) for dig in signal[offset : offset + 8])


def test_part1() -> None:
    """
    Examples for Part 1.
    """
    seq = (1, 2, 3, 4, 5, 6, 7, 8)
    pats = patterns(seq)
    assert pats[1] == (
        0,
        1,
        1,
        0,
        0,
        -1,
        -1,
        0,
    )
    assert pats[2] == (0, 0, 1, 1, 1, 0, 0, 0)
    assert fft(seq, 1) == (4, 8, 2, 2, 6, 1, 5, 8)
    assert fft(seq, 2) == (3, 4, 0, 4, 0, 4, 3, 8)
    assert fft(seq, 4) == (0, 1, 0, 2, 9, 4, 9, 8)
    assert (
        fft(
            (
                8,
                0,
                8,
                7,
                1,
                2,
                2,
                4,
                5,
                8,
                5,
                9,
                1,
                4,
                5,
                4,
                6,
                6,
                1,
                9,
                0,
                8,
                3,
                2,
                1,
                8,
                6,
                4,
                5,
                5,
                9,
                5,
            ),
            100,
        )[:8]
        == (2, 4, 1, 7, 6, 1, 7, 6)
    )
    assert (
        fft(
            (
                1,
                9,
                6,
                1,
                7,
                8,
                0,
                4,
                2,
                0,
                7,
                2,
                0,
                2,
                2,
                0,
                9,
                1,
                4,
                4,
                9,
                1,
                6,
                0,
                4,
                4,
                1,
                8,
                9,
                9,
                1,
                7,
            ),
            100,
        )[:8]
        == (7, 3, 7, 4, 5, 4, 1, 8)
    )


def test_part2() -> None:
    """
    Examples for Part 2.
    """
    fft_real("03036732577212944063491565474664") == "84462026"
    fft_real("02935109699940807407585447034323") == "78725270"
    fft_real("03081770884921959731165446850517") == "53553731"


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2019, day=16)

    seq = tuple(int(dig) for dig in data)
    print(f"Part 1: {''.join(str(dig) for dig in fft(seq, 100)[:8])}")

    print(f"Part 2: {fft_real(data)}")


if __name__ == "__main__":
    main()
