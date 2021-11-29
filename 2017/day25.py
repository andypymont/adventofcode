"""
2017 Day 25
https://adventofcode.com/2017/day/25
"""

from dataclasses import dataclass
from typing import Iterator, Dict, List, Sequence
import re
import aocd # type: ignore

RE_INITIAL = re.compile(r'Begin in state (\w).')
RE_STEPS = re.compile(r'Perform a diagnostic checksum after (\d+) steps.')
RE_STATE = re.compile(r'In state (\w):\s+If the current value is 0:\s+- Write the value (\d+).\s+- Move one slot to the (\w+).\s+- Continue with state (\w).\s+If the current value is 1:\s+- Write the value (\d+).\s+- Move one slot to the (\w+).\s+- Continue with state (\w)')

@dataclass(frozen=True)
class StateInstruction():
    state: str
    current_value: int
    write_value: int
    move: str
    next_state: str

    @classmethod
    def both_from_regex_match(cls, match: Sequence[str]) -> Iterator['StateInstruction']:
        state, zero_write, zero_move, zero_next, one_write, one_move, one_next = match
        yield cls(state, 0, int(zero_write), zero_move, zero_next)
        yield cls(state, 1, int(one_write), one_move, one_next)

    @classmethod
    def all_from_regex_matches(
        cls,
        matches: Sequence[Sequence[str]]
    ) -> Sequence['StateInstruction']:
        instructions: List['StateInstruction'] = []
        for match in matches:
            instructions.extend(cls.both_from_regex_match(match))
        return instructions

@dataclass
class Tape():
    tape: Dict[int, int]
    position: int

    @classmethod
    def new_empty_tape(cls) -> 'Tape':
        return cls({}, 0)

    @property
    def diagnostic_checksum(self) -> int:
        return sum(1 for value in self.tape.values() if value == 1)

    def move(self, direction: str) -> None:
        self.position += (1 if direction == 'right' else -1)

    def read(self) -> int:
        return self.tape.get(self.position, 0)

    def write(self, value: int) -> None:
        self.tape[self.position] = value

@dataclass
class Program():
    tape: Tape
    instructions: Sequence[StateInstruction]
    steps: int
    state: str

    @classmethod
    def from_input_text(cls, text: str) -> 'Program':
        tape = Tape.new_empty_tape()
        instructions = StateInstruction.all_from_regex_matches(RE_STATE.findall(text))
        steps = int(RE_STEPS.findall(text)[0])
        state = RE_INITIAL.findall(text)[0]
        return cls(tape, instructions, steps, state)

    def next_step(self) -> None:
        instruction = next(i for i in self.instructions
                           if i.state == self.state and i.current_value == self.tape.read())
        self.tape.write(instruction.write_value)
        self.tape.move(instruction.move)
        self.state = instruction.next_state
        self.steps -= 1

    def run(self) -> int:
        while self.steps > 0:
            self.next_step()
        return self.tape.diagnostic_checksum

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2017, day=25)
    program = Program.from_input_text(data)
    print(f'Part 1: {program.run()}')

if __name__ == '__main__':
    main()
