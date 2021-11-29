"""
2017 Day 12
https://adventofcode.com/2017/day/12
"""

from typing import Dict, Optional, Sequence, Set, Tuple
import aocd # type: ignore
import regex as re # type: ignore

Pipes = Dict[int, Set[int]]

re_pipes = re.compile(r'(\d+) <-> ([\d ,]+)')
def read_pipes(text: str) -> Pipes:
    pipes: Dict[int, Set[int]] = {}
    for pipe, connections in re_pipes.findall(text):
        pipes[int(pipe)] = set(int(conn) for conn in connections.split(','))
    return pipes

def all_connected_programs(
    pipes: Pipes,
    origin: int = 0,
    visited: Optional[Set[int]] = None
) -> Set[int]:
    visited = visited if visited else set()
    visited.add(origin)
    for pipe in pipes.get(origin, set()):
        if pipe not in visited:
            visited = visited.union(all_connected_programs(pipes, pipe, visited))
    return visited

def find_all_groups(pipes: Pipes) -> Sequence[Sequence[int]]:
    mapped: Set[int] = set()
    groups: Tuple[Sequence[int], ...] = tuple()
    while len(mapped) < len(pipes):
        candidate = next(pipe for pipe in pipes.keys() if pipe not in mapped)
        newly_reached = all_connected_programs(pipes, candidate)
        groups += (newly_reached,)
        mapped = mapped.union(newly_reached)
    return groups

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2017, day=12)

    pipes = read_pipes(data)
    groups = find_all_groups(pipes)

    print(f'Part 1: {next(len(group) for group in groups if 0 in group)}')
    print(f'Part 2: {len(groups)}')

if __name__ == '__main__':
    main()
