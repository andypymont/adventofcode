"""
2017 Day 24
https://adventofcode.com/2017/day/24
"""

from collections import deque
from dataclasses import dataclass
from typing import Iterator, Sequence, Tuple
import aocd # type: ignore

Component = Tuple[int, int]
Components = Tuple[Component, ...]
FlippedStatuses = Tuple[bool, ...]

def read_component(line: str) -> Component:
    first, second = [int(value) for value in line.split('/')]
    return (first, second)

def read_components(text: str) -> Components:
    return tuple(read_component(line) for line in text.split('\n'))

@dataclass(frozen=True)
class Bridge():
    components: Components
    flipped: FlippedStatuses

    @classmethod
    def new_empty_bridge(cls) -> 'Bridge':
        components = ((0, 0),)
        flipped = (False,)
        return cls(components, flipped)

    @property
    def strength(self) -> int:
        return sum(sum(component) for component in self.components)

    @property
    def length(self) -> int:
        return len(self.components)

    @property
    def end(self) -> int:
        one, two = self.components[-1]
        return one if self.flipped[-1] else two

    def is_extendable_by(self, component: Component) -> bool:
        return self.end in component

    def extend(self, component: Component) -> 'Bridge':
        new_components = self.components + (component,)
        new_flipped = self.flipped + (component[1] == self.end,)
        return Bridge(new_components, new_flipped)

    def all_possible_extensions(self, components: Components) -> Sequence['Bridge']:
        unused = (component for component in components if component not in self.components)
        return tuple(
            self.extend(component)
            for component in unused
            if self.is_extendable_by(component)
        )

def find_all_bridges(components: Components) -> Iterator[Bridge]:
    consider: deque = deque()
    consider.append(Bridge.new_empty_bridge())

    while len(consider) > 0:
        bridge = consider.popleft()
        options = bridge.all_possible_extensions(components)
        if len(options) == 0:
            yield bridge
        consider.extend(options)

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2017, day=24)
    components = read_components(data)
    bridges = tuple(find_all_bridges(components))
    part1 = max(bridge.strength for bridge in bridges)
    print(f'Part 1: {part1}')

    max_length = max(bridge.length for bridge in bridges)
    part2 = max(bridge.strength for bridge in bridges if bridge.length == max_length)
    print(f'Part 2: {part2}')

if __name__ == '__main__':
    main()
