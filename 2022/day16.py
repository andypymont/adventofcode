"""
2022 Day 16
https://adventofcode.com/2022/day/16
"""

from heapq import heappop, heappush
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


@dataclass(frozen=True)
class State:
    """
    A state that can be reached during an attempt to find the solution to the problem: this
    consists of the current location, the currently-open valves, the time in minutes remaining, and
    the total amount of accrued pressure (including future pressure due between time=0 from valves
    that are already open).
    """

    location: str
    open_valves: frozenset[str]
    time: int
    pressure: int

    def __lt__(self, other: "State") -> bool:
        """
        Compare this State to another. The main intended use case is in a min-heap where highest-
        pressure State objects should be popped first, therefore this returns True if the other
        State has a *lower* pressure.
        """
        return other.pressure < self.pressure

    @classmethod
    def create_initial(cls, valves: dict[str, Valve], time: int) -> "State":
        """
        Return the initial state for the given set of valves. This will mean being located at at AA
        with no time elapsed. We assume all zero-pressure valves are switched on, to avoid ever
        bothering to turn them on later and since they will make no difference to the pressure
        output.
        """
        return cls(
            "AA",
            frozenset(valve.name for valve in valves.values() if valve.flow_rate == 0),
            time,
            0,
        )

    def maximum_potential(self, valves: dict[str, Valve]) -> int:
        """
        Calculate the maximum possible potential for this state, if all other valves were instantly
        opened by a benevolent omnipotent passerby.
        """
        extra_pressure = self.time * sum(
            valve.flow_rate
            for valve in valves.values()
            if valve.name not in self.open_valves
        )
        return self.pressure + extra_pressure

    def open_valve(self, valve: Valve) -> "State":
        """
        Return a modified version of this state after spending one minute opening the given valve.
        """
        new_pressure = (self.time - 1) * valve.flow_rate
        return State(
            self.location,
            self.open_valves | {valve.name},
            self.time - 1,
            self.pressure + new_pressure,
        )

    def move(self, location: str) -> "State":
        """
        Return a modified version of this state after spending one minute moving to the given
        location.
        """
        return State(location, self.open_valves, self.time - 1, self.pressure)

    def reachable(self, valves: dict[str, Valve]) -> set["State"]:
        """
        Return the set of reachable states for this one, given the known set of valves.

        This will consist of:
        - Opening the current value (taking one minute)
        - Moving to each reachable location from this one (taking one minute)
        """
        reachable: set[State] = set()

        if self.time > 0:
            if self.location not in self.open_valves:
                reachable.add(self.open_valve(valves[self.location]))

            for neighbour in valves[self.location].tunnels:
                reachable.add(self.move(neighbour))

        return reachable


def most_pressure_possible(valves: dict[str, Valve]) -> int:
    """
    Conduct a search of all possible movements within the given set of valves and return the
    highest possible total pressure that can be generated in 30 minutes.
    """
    consider = [State.create_initial(valves, 30)]
    visited: dict[tuple[str, frozenset[str]], int] = {}
    best_pressure = 0

    while consider:
        state = heappop(consider)

        # update best pressure estimate if this state will end up bettering it
        if state.pressure > best_pressure:
            best_pressure = state.pressure

        # stop if we've run out of time
        if state.time == 0:
            continue

        # discard this state if it can no longer do as well as the best existing solution
        potential = state.maximum_potential(valves)
        if potential < best_pressure:
            continue

        # discard this state if we've been in this location before but with more potential
        position = (state.location, state.open_valves)
        if visited.get(position, 0) >= potential:
            continue
        visited[position] = potential

        # consider all other reachable states from this one
        for next_state in state.reachable(valves):
            heappush(consider, next_state)

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

    best_route = (
        State("AA", frozenset(("AA", "FF", "GG", "II")), 30, 0),
        State("DD", frozenset(("AA", "FF", "GG", "II")), 29, 0),
        State("DD", frozenset(("AA", "DD", "FF", "GG", "II")), 28, 560),
        State("CC", frozenset(("AA", "DD", "FF", "GG", "II")), 27, 560),
        State("BB", frozenset(("AA", "DD", "FF", "GG", "II")), 26, 560),
        State("BB", frozenset(("AA", "BB", "DD", "FF", "GG", "II")), 25, 885),
        State("AA", frozenset(("AA", "BB", "DD", "FF", "GG", "II")), 24, 885),
        State("II", frozenset(("AA", "BB", "DD", "FF", "GG", "II")), 23, 885),
        State("JJ", frozenset(("AA", "BB", "DD", "FF", "GG", "II")), 22, 885),
        State("JJ", frozenset(("AA", "BB", "DD", "FF", "GG", "II", "JJ")), 21, 1326),
        State("II", frozenset(("AA", "BB", "DD", "FF", "GG", "II", "JJ")), 20, 1326),
        State("AA", frozenset(("AA", "BB", "DD", "FF", "GG", "II", "JJ")), 19, 1326),
        State("DD", frozenset(("AA", "BB", "DD", "FF", "GG", "II", "JJ")), 18, 1326),
        State("EE", frozenset(("AA", "BB", "DD", "FF", "GG", "II", "JJ")), 17, 1326),
        State("FF", frozenset(("AA", "BB", "DD", "FF", "GG", "II", "JJ")), 16, 1326),
        State("GG", frozenset(("AA", "BB", "DD", "FF", "GG", "II", "JJ")), 15, 1326),
        State("HH", frozenset(("AA", "BB", "DD", "FF", "GG", "II", "JJ")), 14, 1326),
        State(
            "HH", frozenset(("AA", "BB", "DD", "FF", "GG", "HH", "II", "JJ")), 13, 1612
        ),
        State(
            "GG", frozenset(("AA", "BB", "DD", "FF", "GG", "HH", "II", "JJ")), 12, 1612
        ),
        State(
            "FF", frozenset(("AA", "BB", "DD", "FF", "GG", "HH", "II", "JJ")), 11, 1612
        ),
        State(
            "EE", frozenset(("AA", "BB", "DD", "FF", "GG", "HH", "II", "JJ")), 10, 1612
        ),
        State(
            "EE",
            frozenset(("AA", "BB", "DD", "EE", "FF", "GG", "HH", "II", "JJ")),
            9,
            1639,
        ),
        State(
            "DD",
            frozenset(("AA", "BB", "DD", "EE", "FF", "GG", "HH", "II", "JJ")),
            8,
            1639,
        ),
        State(
            "CC",
            frozenset(("AA", "BB", "DD", "EE", "FF", "GG", "HH", "II", "JJ")),
            7,
            1639,
        ),
        State(
            "CC",
            frozenset(("AA", "BB", "CC", "DD", "EE", "FF", "GG", "HH", "II", "JJ")),
            6,
            1651,
        ),
        State(
            "DD",
            frozenset(("AA", "BB", "CC", "DD", "EE", "FF", "GG", "HH", "II", "JJ")),
            5,
            1651,
        ),
        State(
            "CC",
            frozenset(("AA", "BB", "CC", "DD", "EE", "FF", "GG", "HH", "II", "JJ")),
            4,
            1651,
        ),
        State(
            "DD",
            frozenset(("AA", "BB", "CC", "DD", "EE", "FF", "GG", "HH", "II", "JJ")),
            3,
            1651,
        ),
        State(
            "CC",
            frozenset(("AA", "BB", "CC", "DD", "EE", "FF", "GG", "HH", "II", "JJ")),
            2,
            1651,
        ),
        State(
            "DD",
            frozenset(("AA", "BB", "CC", "DD", "EE", "FF", "GG", "HH", "II", "JJ")),
            1,
            1651,
        ),
        State(
            "CC",
            frozenset(("AA", "BB", "CC", "DD", "EE", "FF", "GG", "HH", "II", "JJ")),
            0,
            1651,
        ),
    )

    assert State.create_initial(valves, 30) == best_route[0]
    assert best_route[0].reachable(valves) == {
        State("BB", frozenset(("AA", "FF", "GG", "II")), 29, 0),
        best_route[1],
        State("II", frozenset(("AA", "FF", "GG", "II")), 29, 0),
    }
    assert best_route[1].reachable(valves) == {
        best_route[2],
        State("AA", frozenset(("AA", "FF", "GG", "II")), 28, 0),
        State("CC", frozenset(("AA", "FF", "GG", "II")), 28, 0),
        State("EE", frozenset(("AA", "FF", "GG", "II")), 28, 0),
    }

    for pos in range(1, 31):
        assert best_route[pos] in best_route[pos - 1].reachable(valves)

    assert best_route[0].maximum_potential(valves) == 2430
    assert best_route[27].maximum_potential(valves) == 1651

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
