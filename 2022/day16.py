"""
2022 Day 16
https://adventofcode.com/2022/day/16
"""

from collections import deque
from dataclasses import dataclass
import re
import aocd  # type: ignore

re_valve = re.compile(
    r"Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? ([\w, ]+)"
)


@dataclass(frozen=True)
class Valve:
    """
    One of the pressure valves in the maze.
    """

    name: str
    flow_rate: int
    tunnels: frozenset[str]

    @classmethod
    def from_text(cls, text: str) -> "Valve":
        """
        Read a Valve from its description in a single line of the puzzle input.
        """
        if not (match := re_valve.match(text)):
            raise ValueError(f"Could not find Valve description in line {repr(text)}")

        return cls(
            match.groups()[0],
            int(match.groups()[1]),
            frozenset(match.groups()[2].split(", ")),
        )

    @classmethod
    def all_from_text(cls, text: str) -> dict[str, "Valve"]:
        """
        Read all Valves from the given puzzle input and return a dictionary mapping valve names to
        Valve objects.
        """
        return {
            valve.name: valve
            for valve in (Valve.from_text(line) for line in text.splitlines())
        }


def shortest_distance_graph(valves: dict[str, Valve]) -> dict[tuple[str, str], int]:
    """
    Explore the connections between the given valves and return a dictionary which contains
    key-value pairs where each key is a pair of locations e.g. ("AA", "DD") and the corresponding
    value is the shortest distance between them.
    """
    graph: dict[tuple[str, str], int] = {}

    for start in valves.keys():
        visited: set[str] = set()
        consider = deque([(start, 0)])

        while consider:
            location, steps = consider.popleft()
            if location in visited:
                continue
            visited.add(location)
            if location != start:
                graph[(start, location)] = steps
            for adjacent in valves[location].tunnels:
                consider.append((adjacent, steps + 1))

    return graph


@dataclass(frozen=True)
class State:
    """
    A state that can be reached during an attempt to find the solution to the problem: this
    consists of the current location, time, open valves, and the pressure accumulating each minute.
    """

    location: str
    time: int
    open_valves: frozenset[str]
    ppm: int

    @classmethod
    def create_initial(cls, valves: dict[str, Valve]) -> "State":
        """
        Return the initial state for the given set of valves. This will mean being located at at AA
        with no time elapsed. We assume all zero-pressure valves are switched on, to avoid ever
        bothering to turn them on later and since they will make no difference to the pressure
        output.
        """
        return cls(
            "AA",
            0,
            frozenset(valve.name for valve in valves.values() if valve.flow_rate == 0),
            0,
        )

    def reachable(
        self, valves: dict[str, Valve], graph: dict[tuple[str, str], int]
    ) -> set["State"]:
        """
        Return the set of reachable states for this one, given the known set of valves and the
        graph of shortest travel distances between them.

        This will consist of:
        - Waiting in the current valve until 30 minutes total have passed
        - Moving to each non-open valve and opening it
        """
        reachable: set[State] = set()

        if (minutes := 30 - self.time) > 0:
            reachable.add(
                State(self.location, self.time + minutes, self.open_valves, self.ppm)
            )

        for valve in valves.values():
            if valve.name not in self.open_valves:
                reachable.add(
                    State(
                        valve.name,
                        self.time + graph[(self.location, valve.name)] + 1,
                        self.open_valves | {valve.name},
                        self.ppm + valve.flow_rate,
                    )
                )

        return reachable


def most_pressure_possible(valves: dict[str, Valve]) -> int:
    """
    Conduct a search of all possible movements within the given set of valves and return the
    highest possible total pressure that can be generated in 30 minutes.
    """
    graph = shortest_distance_graph(valves)
    consider = deque([(State.create_initial(valves), 0)])
    best_pressure = 0
    all_open_pressure = sum(valve.flow_rate for valve in valves.values())

    while consider:
        state, pressure = consider.popleft()

        # discard invalid states (i.e. took too long to travel to this valve)
        if state.time > 30:
            continue

        # if we're at minute 30, either discard or record this solution based on how it compares to
        # the existing best solution
        if state.time == 30:
            if pressure > best_pressure:
                best_pressure = pressure
            continue

        # discard this state if it can no longer do as well as our best existing solution
        max_achievable_pressure = pressure + ((30 - state.time) * all_open_pressure)
        if max_achievable_pressure < best_pressure:
            continue

        # consider all other reachable states from this one
        for next_state in state.reachable(valves, graph):
            time_elapsed = next_state.time - state.time
            next_pressure = pressure + (state.ppm * time_elapsed)
            consider.append((next_state, next_pressure))

    return best_pressure


def test_part1() -> None:
    """
    Examples for Part 1.
    """
    assert Valve.from_text(
        "Valve AA has flow rate=0; tunnels lead to valves DD, II, BB"
    ) == Valve("AA", 0, frozenset(("DD", "II", "BB")))
    assert Valve.from_text(
        "Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE"
    ) == Valve("DD", 20, frozenset(("CC", "AA", "EE")))
    assert Valve.from_text(
        "Valve HH has flow rate=22; tunnel leads to valve GG"
    ) == Valve("HH", 22, frozenset(("GG",)))
    valves = {
        "AA": Valve("AA", 0, frozenset(("DD", "II", "BB"))),
        "BB": Valve("BB", 13, frozenset(("CC", "AA"))),
        "CC": Valve("CC", 2, frozenset(("DD", "BB"))),
        "DD": Valve("DD", 20, frozenset(("CC", "AA", "EE"))),
        "EE": Valve("EE", 3, frozenset(("FF", "DD"))),
        "FF": Valve("FF", 0, frozenset(("EE", "GG"))),
        "GG": Valve("GG", 0, frozenset(("FF", "HH"))),
        "HH": Valve("HH", 22, frozenset(("GG",))),
        "II": Valve("II", 0, frozenset(("AA", "JJ"))),
        "JJ": Valve("JJ", 21, frozenset(("II",))),
    }
    assert (
        Valve.all_from_text(
            "\n".join(
                (
                    "Valve AA has flow rate=0; tunnels lead to valves DD, II, BB",
                    "Valve BB has flow rate=13; tunnels lead to valves CC, AA",
                    "Valve CC has flow rate=2; tunnels lead to valves DD, BB",
                    "Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE",
                    "Valve EE has flow rate=3; tunnels lead to valves FF, DD",
                    "Valve FF has flow rate=0; tunnels lead to valves EE, GG",
                    "Valve GG has flow rate=0; tunnels lead to valves FF, HH",
                    "Valve HH has flow rate=22; tunnel leads to valve GG",
                    "Valve II has flow rate=0; tunnels lead to valves AA, JJ",
                    "Valve JJ has flow rate=21; tunnel leads to valve II",
                )
            )
        )
        == valves
    )
    graph = shortest_distance_graph(valves)
    assert len(graph) == 90
    assert graph[("AA", "BB")] == 1
    assert graph[("AA", "EE")] == 2
    assert graph[("FF", "AA")] == 3
    assert graph[("JJ", "BB")] == 3

    one = State("AA", 0, frozenset(("AA", "FF", "GG", "II")), 0)
    assert State.create_initial(valves) == one
    assert one.reachable(valves, graph) == {
        State("AA", 30, frozenset(("AA", "FF", "GG", "II")), 0),
        State("BB", 2, frozenset(("AA", "BB", "FF", "GG", "II")), 13),
        State("CC", 3, frozenset(("AA", "CC", "FF", "GG", "II")), 2),
        State("DD", 2, frozenset(("AA", "DD", "FF", "GG", "II")), 20),
        State("EE", 3, frozenset(("AA", "EE", "FF", "GG", "II")), 3),
        State("HH", 6, frozenset(("AA", "FF", "GG", "HH", "II")), 22),
        State("JJ", 3, frozenset(("AA", "FF", "GG", "II", "JJ")), 21),
    }

    assert most_pressure_possible(valves) == 1651


# def test_part2() -> None:
#     """
#     Examples for Part 2.
#     """
#     assert False


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2022, day=16)
    valves = Valve.all_from_text(data)

    print(f"Part 1: {most_pressure_possible(valves)}")
    # print(f'Part 2: {p2}')


if __name__ == "__main__":
    main()
