"""
2016 Day 9
https://adventofcode.com/2016/day/9
"""

import aocd # type: ignore

def decompressed_len(text: str, nested_tags: bool = False) -> int:
    """
    Return the length of the given string once decompressed.
    """
    pos = in_tag = capture = 0
    lengths = [1] * len(text)

    while pos < len(text):
        if capture > 0 and not nested_tags:
            capture -= 1
        elif text[pos] == '(':
            in_tag, tag = True, ''

        if in_tag:
            lengths[pos] = 0
            tag += text[pos]
            if text[pos] == ')':
                in_tag = False
                capture, repeat = [int(x) for x in tag[1:-1].lower().split('x')]
                for offset in range(capture):
                    lengths[pos + 1 + offset] *= repeat

        pos += 1

    return sum(lengths)

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2016, day=9)

    print(f'Part 1: {decompressed_len(data)}')
    print(f'Part 2: {decompressed_len(data, nested_tags=True)}')

if __name__ == '__main__':
    main()
