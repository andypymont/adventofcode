"""
2020 Day 19
https://adventofcode.com/2020/day/19
"""

from typing import Dict, Sequence
import aocd # type: ignore
import regex # type: ignore

def read_rules(text: str) -> Dict[str, str]:
    return {line[0]: line[1] for line in [line.split(': ') for line in text.split('\n')]}

def read_messages(text: str) -> Sequence[str]:
    return text.split('\n')

def regex_rule(rule: str, rules: Dict[str, str]) -> str:
    if '"' in rule:
        return rule[1]
    parts = rule.split('|')
    if len(parts) > 1:
        return '(?:' + '|'.join(regex_rule(part, rules) for part in parts) + ')'
    parts = parts[0].split(' ')
    return ''.join(regex_rule(rules[part], rules) for part in parts if part)

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2020, day=19)

    rulesdata, messagesdata = data.split('\n\n')
    rules = read_rules(rulesdata)
    messages = read_messages(messagesdata)
    rule = regex_rule(rules['0'], rules)
    part1 = sum(1 for message in messages if regex.fullmatch(rule, message))
    print(f'Part 1: {part1}')

    rules2 = dict(**rules)
    rules2.update(**{'8': '42 | 42 8', '11': '42 31 | 42 11 31'})

    # >> [(number, content) for number, content in rules2.items()
    #     if '8' in content.split(' ') or '11' in content.split(' ')]
    # .. [('0', '8 11'), ('8', '42 | 42 8'), ('11', '42 31 | 42 11 31')]

    # So rules 8 and 11 apear only in themselves and rule 0
    # - Rule 8: rule 42 any number of times
    # - Rule 11: any number of 42s followed by the same number of 31s
    # Rewrite these and run rule 0 and we're there

    fortytwo = regex_rule(rules2['42'], rules2)
    thirtyone = regex_rule(rules2['31'], rules2)
    eight = '(?:42)+'.replace('42', fortytwo)
    eleven = '((?:4231)|(?:42(?1)31))'.replace('42', fortytwo).replace('31', thirtyone)
    zero = eight + eleven
    part2 = sum(1 for message in messages if regex.fullmatch(zero, message))
    print(f'Part 2: {part2}')

if __name__ == '__main__':
    main()
