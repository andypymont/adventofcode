"""
2015 Day 19
https://adventofcode.com/2015/day/19
"""

from dataclasses import dataclass
from typing import Set
import aocd # type: ignore

@dataclass(frozen=True)
class Replacement:
    """
    Represents a valid replacement that can be made within a molecule.
    """
    replace: str
    replace_with: str

    def reverse(self) -> 'Replacement':
        """
        Return a reversed version of the replacement (to be used to goal-seek in the opposite
        direction to manage the size of the solution space).
        """
        return self.__class__(self.replace_with, self.replace)

    @classmethod
    def all_from_input(cls, text: str) -> 'Set[Replacement]':
        """
        Parse all replacements from the puzzle input.
        """
        replacements = set()
        for line in text.split('\n'):
            if ' => ' in line:
                parts = line.split(' => ')
                if len(parts) == 2:
                    replacements.add(cls(parts[0], parts[1]))
        return replacements

def possible_moves(molecule: str, replacements: Set[Replacement]) -> Set[str]:
    """
    Given the set of available replacements and the current molecule, determine which possible
    resulting molecules can be moved to from this state.
    """
    possible = set()
    for replacement in replacements:
        for start in range(len(molecule)):
            end = start + len(replacement.replace)
            if molecule[start:end] == replacement.replace:
                possible.add(molecule[:start] + replacement.replace_with + molecule[end:])
    return possible

def fewest_steps(replacements: Set[Replacement], target: str) -> int:
    """
    Identify the fewest number of steps needed to transform 'e' into the medicine - by goal-seeking
    in the opposite direction.
    """
    words = {}
    attempts = [target]
    words[target] = 0

    replacements = {replacement.reverse() for replacement in replacements}

    while attempts:
        candidate = attempts.pop(0)
        steps = words[candidate]

        if candidate == 'e':
            return steps

        for next_step in possible_moves(candidate, replacements):
            if next_step not in words:
                words[next_step] = (steps + 1)
                attempts.append(next_step)
            elif words[next_step] > (steps + 1):
                words[next_step] = (steps + 1)
        attempts.sort(key=len)

    return -1

def main():
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2015, day=19)

    replacements = Replacement.all_from_input(data)
    medicine = data.split('\n')[-1]

    print(f'Part 1: {len(possible_moves(medicine, replacements))}')
    print(f'Part 2: {fewest_steps(replacements, medicine)}')

if __name__ == '__main__':
    main()
