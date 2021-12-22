"""
2021 Day 8
https://adventofcode.com/2021/day/8
"""

from typing import Dict, Iterable, List, Set, Tuple
import aocd  # type: ignore

Display = Tuple[Set[str], Tuple[str, ...]]


def read_displays(text: str) -> List[Display]:
    return [read_display(line) for line in text.split("\n")]


def read_display(text: str) -> Display:
    sections = text.split(" | ")
    patterns = set(sort_str(p) for p in sections[0].split(" "))
    outputs = tuple(sort_str(o) for o in sections[1].split(" "))
    return (patterns, outputs)


def unique_outputs(displays: Iterable[Display]) -> int:
    return sum(
        sum(1 for output in outputs if len(output) in (2, 3, 4, 7))
        for _, outputs in displays
    )


def sort_str(original: str) -> str:
    return "".join(sorted(original))


def decode_patterns(display: Display) -> Dict[str, int]:
    patterns = display[0]
    wires: Dict[str, str] = {}
    decoded: Dict[int, str] = {}

    # Begin by identifying the unique-length values 1, 4, 7, and 8:
    decoded[1] = next(p for p in patterns if len(p) == 2)
    decoded[4] = next(p for p in patterns if len(p) == 4)
    decoded[7] = next(p for p in patterns if len(p) == 3)
    decoded[8] = next(p for p in patterns if len(p) == 7)

    # This allows us to pin down wire 'a' as it's in 7 and not in 1:
    wires["a"] = next(l for l in decoded[7] if l not in decoded[1])

    # We can also identify some of the wires by how often they appear:
    wires["b"] = next(l for l in "abcdefg" if sum(1 for p in patterns if l in p) == 6)
    wires["e"] = next(l for l in "abcdefg" if sum(1 for p in patterns if l in p) == 4)
    wires["f"] = next(l for l in "abcdefg" if sum(1 for p in patterns if l in p) == 9)

    # And knowing wire 'a', similar logic finds wire 'c':
    wires["c"] = next(
        l
        for l in "abcdefg"
        if sum(1 for p in patterns if l in p) == 8 and l != wires["a"]
    )

    # We can now use these known wires to identify some more of the patterns:
    decoded[3] = next(
        p
        for p in patterns
        if len(p) == 5 and wires["b"] not in p and wires["e"] not in p
    )
    decoded[5] = next(
        p
        for p in patterns
        if len(p) == 5 and wires["c"] not in p and wires["e"] not in p
    )
    decoded[6] = next(p for p in patterns if len(p) == 6 and wires["c"] not in p)
    decoded[9] = next(p for p in patterns if len(p) == 6 and wires["e"] not in p)

    # And by a process of elimination, this leaves two remaining patterns:
    decoded[0] = next(
        p for p in patterns if len(p) == 6 and p not in {decoded[6], decoded[9]}
    )
    decoded[2] = next(
        p for p in patterns if len(p) == 5 and p not in {decoded[3], decoded[5]}
    )

    return {pattern: value for value, pattern in decoded.items()}


def decode_output(display: Display) -> int:
    decode = decode_patterns(display)
    return int("".join(str(decode[output]) for output in display[1]))


def test_part1() -> None:
    """
    Examples for Part 1.
    """
    ex1 = "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"
    eg1 = (
        {
            "abcdefg",
            "bcdef",
            "acdfg",
            "abcdf",
            "abd",
            "abcdef",
            "bcdefg",
            "abef",
            "abcdeg",
            "ab",
        },
        ("bcdef", "abcdf", "bcdef", "abcdf"),
    )
    assert read_display(ex1) == eg1
    eg2 = read_displays(
        "\n".join(
            (
                "be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe",
                "edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc",
                "fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg",
                "fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb",
                "aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea",
                "fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb",
                "dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe",
                "bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef",
                "egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb",
                "gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce",
            )
        )
    )
    assert unique_outputs(eg2) == 26


def test_part2() -> None:
    """
    Examples for Part 2.
    """
    example = (
        {
            "abcdefg",
            "bcdef",
            "acdfg",
            "abcdf",
            "abd",
            "abcdef",
            "bcdefg",
            "abef",
            "abcdeg",
            "ab",
        },
        ("bcdef", "abcdf", "bcdef", "abcdf"),
    )
    assert decode_patterns(example) == {
        "abcdefg": 8,
        "bcdef": 5,
        "acdfg": 2,
        "abcdf": 3,
        "abd": 7,
        "abcdef": 9,
        "bcdefg": 6,
        "abef": 4,
        "abcdeg": 0,
        "ab": 1,
    }
    assert decode_output(example) == 5353


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2021, day=8)
    displays = read_displays(data)

    print(f"Part 1: {unique_outputs(displays)}")
    print(f"Part 2: {sum(decode_output(display) for display in displays)}")


if __name__ == "__main__":
    main()
