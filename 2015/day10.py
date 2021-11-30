"""
2015 Day 10
https://adventofcode.com/2015/day/10
"""

import aocd # type: ignore


def look_and_say(word: str) -> str:
    """
    Replace each repeated pattern of digits in the given string with a set of characters describing
    the repeated pattern.
    """
    result = ''
    prev = word[0]
    current_run = 0

    for char in word:
        if char == prev:
            current_run += 1
        else:
            result += str(current_run) + prev
            prev = char
            current_run = 1

    return result + str(current_run) + prev

def look_and_say_repeatedly(word: str, times: int) -> str:
    """
    Repeatedly run look_and_say over the same phrase.
    """
    for _ in range(times):
        word = look_and_say(word)
    return word

def test_example():
    """
    Examples from the puzzle description.
    """
    assert look_and_say('1') == '11'
    assert look_and_say('11') == '21'
    assert look_and_say('21') == '1211'
    assert look_and_say('1211') == '111221'
    assert look_and_say_repeatedly('1', 5) == '312211'

def main():
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2015, day=10)

    repeated = look_and_say_repeatedly(data, 40)
    print(f'Part 1: {len(repeated)}')

    repeated = look_and_say_repeatedly(repeated, 10)
    print(f'Part 2: {len(repeated)}')

if __name__ == '__main__':
    main()
