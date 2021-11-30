"""
2015 Day 9
https://adventofcode.com/2015/day/9
"""

from itertools import permutations
from typing import Dict, Iterable, Sequence
import aocd # type: ignore

RoutingTable = Dict[str, Dict[str, int]]
Route = Sequence[str]

def read_routing(text: str) -> RoutingTable:
    """
    Create a routing table based on the provided information about distances.
    """
    routes: Dict[str, Dict[str, int]] = {}
    for line in text.split('\n'):
        origin, dest, dist = line.replace(' to ', ' = ').split(' = ')
        if origin not in routes:
            routes[origin] = {}
        routes[origin][dest] = int(dist)
        if dest not in routes:
            routes[dest] = {}
        routes[dest][origin] = int(dist)
    return routes

def all_possible_routes(routing: RoutingTable) -> Iterable[Route]:
    """
    Calculate every possible permutation of routing through the locations, based on the routing
    table provided.
    """
    locations = routing.keys()
    return permutations(locations, len(locations))

def route_length(routing: RoutingTable, route: Route) -> int:
    """
    Calculate the length of a route, by adding up the distances of each step as per the provided
    routing table.
    """
    steps = [route[x:x+2] for x in range(len(route) - 1)]
    return sum(
        routing.get(origin, {}).get(dest, 0) for (origin, dest) in steps
    )

def all_route_lengths(routing: RoutingTable) -> Iterable[int]:
    """
    Calculate all possible route lengths for the given routing table.
    """
    for route in all_possible_routes(routing):
        yield route_length(routing, route)

def test_example():
    """
    Test case from puzzle description.
    """
    example = '\n'.join((
        'London to Dublin = 464',
        'London to Belfast = 518',
        'Dublin to Belfast = 141'
    ))
    routing = read_routing(example)
    lengths = tuple(all_route_lengths(routing))
    assert len(lengths) == 6
    assert set(lengths) == {605, 659, 982}

def main():
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2015, day=9)
    routing = read_routing(data)
    lengths = set(all_route_lengths(routing))

    print(f'Part 1: {min(lengths)}')
    print(f'Part 2: {max(lengths)}')

if __name__ == '__main__':
    main()
