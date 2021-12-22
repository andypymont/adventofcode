"""
2016 Day 7
https://adventofcode.com/2016/day/7
"""

import re
from typing import Any, Iterable, Sequence
import aocd  # type: ignore

RE_HYPERNET = re.compile(r"(\[\w+\])")
RE_ABBA = re.compile(r"(\w)((?!\1)\w)(\2)(\1)")
RE_ABA = re.compile(r"(\w)((?!\1)\w)(\1)")


def findall(pattern: re.Pattern, text: str) -> Iterable[Sequence[Any]]:
    """
    In the style of regex.findall(text), but allowing for overlapping groups.
    """
    reported = set()
    pos = 0
    while pos < len(text):
        match = pattern.search(text, pos)
        if match:
            if match.start() not in reported:
                yield match.groups()
                reported.add(match.start())
        pos += 1


def reverse_aba(aba: str) -> str:
    """
    Calculate the reverse of an 'aba' (e.g. 'efe' becomes 'fef')
    """
    return aba[1] + aba[0] + aba[1]


def hypernet(string: str) -> Sequence[str]:
    """
    Return the hypernet sequences in the given string, i.e. parts in square brackets.
    """
    return [substr for substr in RE_HYPERNET.split(string) if substr[0] == "["]


def supernet(string: str) -> Sequence[str]:
    """
    Return the supernet sequences in the given string, i.e. i.e. parts not in square brackets.
    """
    return [substr for substr in RE_HYPERNET.split(string) if substr[0] != "["]


def supports_tls(string: str) -> bool:
    """
    Does the address support TLS? i.e. the supernet contains 1+ ABBA and the hypernet does not.
    """
    hypernet_abbas = sum(
        1 for phrase in hypernet(string) if RE_ABBA.search(phrase) is not None
    )
    supernet_abbas = sum(
        1 for phrase in supernet(string) if RE_ABBA.search(phrase) is not None
    )
    return hypernet_abbas == 0 and supernet_abbas > 0


def supports_ssl(string: str) -> bool:
    """
    Does the address support SSL? i.e. there is an ABA in hypernet which is present as BAB in the
    supernet.
    """
    hypernet_abas = [
        "".join(aba) for aba in findall(RE_ABA, "|".join(hypernet(string)))
    ]
    supernet_abas = [
        "".join(aba) for aba in findall(RE_ABA, "|".join(supernet(string)))
    ]
    return sum(1 for aba in supernet_abas if reverse_aba(aba) in hypernet_abas) > 0


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2016, day=7)
    hostnames = data.split("\n")

    print(f"Part 1: {sum(1 for host in hostnames if supports_tls(host))}")
    print(f"Part 2: {sum(1 for host in hostnames if supports_ssl(host))}")


if __name__ == "__main__":
    main()
