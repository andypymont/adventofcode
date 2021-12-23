"""
2021 Day 23
https://adventofcode.com/2021/day/23
"""

from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Set, Tuple
import aocd  # type: ignore


ROOMS = "ABCD"
DOORS = (2, 4, 6, 8)
COSTS = {"A": 1, "B": 10, "C": 100, "D": 1000}


@dataclass(frozen=True, order=True)
class State:
    energy: int
    corridor: str
    rooms: Tuple[str, str, str, str]
    room_size: int

    @classmethod
    def from_input(cls, text: str, part2: bool = False) -> "State":
        lines = text.split("\n")
        return cls(
            0,
            lines[1][1:12],
            (
                lines[2][3] + ("DD" if part2 else "") + lines[3][3],
                lines[2][5] + ("CB" if part2 else "") + lines[3][5],
                lines[2][7] + ("BA" if part2 else "") + lines[3][7],
                lines[2][9] + ("AC" if part2 else "") + lines[3][9],
            ),
            4 if part2 else 2,
        )

    def is_ready(self, room: int) -> bool:
        """
        Return True/False whether the given room is enterable by its intended amphipods, i.e. it
        does not contain any mismatched amphipods.
        """
        return len(set(self.rooms[room]) - {ROOMS[room]}) == 0

    def is_solved(self) -> bool:
        return len(set(self.corridor)) == 1 and all(self.is_ready(r) for r in range(3))

    def distance(self, room: int, position: int) -> int:
        """
        Calculate the distance from the current top of the given room to the given position in the
        corridor. Return the number of steps, or -1 if it can't be reached.
        """
        if position in DOORS:
            return -1

        leave_room = 1 + self.room_size - len(self.rooms[room])
        door = DOORS[room]
        traverse = (
            self.corridor[door:position]
            if door <= position
            else self.corridor[position + 1 : door + 1]
        )

        return leave_room + len(traverse) if set(traverse) == {"."} else -1

    def valid_moves(self) -> Set["State"]:
        moves = set()

        # move type A: move amphipods from the corridor into the room where they belong
        for pos, char in enumerate(self.corridor):
            if char == ".":
                continue
            room = ROOMS.find(char)
            if not self.is_ready(room):
                continue
            dist = self.distance(room, pos)
            if dist == -1:
                continue
            dist -= 1  # no need to enter occupied space within room

            moves.add(
                self.__class__(
                    self.energy + (COSTS[char] * dist),
                    self.corridor[:pos] + "." + self.corridor[pos + 1 :],
                    (
                        self.rooms[0] + (char if room == 0 else ""),
                        self.rooms[1] + (char if room == 1 else ""),
                        self.rooms[2] + (char if room == 2 else ""),
                        self.rooms[3] + (char if room == 3 else ""),
                    ),
                    self.room_size,
                )
            )

        # move type B: move amphipods from non-matching rooms to free positions in the corridor
        for room, contents in enumerate(self.rooms):
            if contents == "" or self.is_ready(room):
                continue
            char = contents[0]
            for pos, there in enumerate(self.corridor):
                if there != ".":
                    continue
                dist = self.distance(room, pos)
                if dist == -1:
                    continue

                contents_without = contents[1:]
                moves.add(
                    self.__class__(
                        self.energy + (COSTS[char] * dist),
                        self.corridor[:pos] + char + self.corridor[pos + 1 :],
                        (
                            contents_without if room == 0 else self.rooms[0],
                            contents_without if room == 1 else self.rooms[1],
                            contents_without if room == 2 else self.rooms[2],
                            contents_without if room == 3 else self.rooms[3],
                        ),
                        self.room_size,
                    )
                )

            if contents:
                char = contents[0]
                if char != ROOMS[room]:
                    for pos in range(len(self.corridor)):
                        dist = self.distance(room, pos)

        return moves

    def solve(self) -> "State":
        queue = [self]
        visited: Set[Tuple[str, Tuple[str, str, str, str]]] = set()

        while queue:
            state = heappop(queue)
            if state.is_solved():
                return state
            if (state.corridor, state.rooms) in visited:
                continue
            visited.add((state.corridor, state.rooms))
            for move in state.valid_moves():
                heappush(queue, move)

        raise ValueError("No valid solution for this state")


def test_part1() -> None:
    """
    Examples for Part 1.
    """
    initial = State(0, "...........", ("BA", "CD", "BC", "DA"), 2)
    assert (
        State.from_input(
            "\n".join(
                (
                    "#############",
                    "#...........#",
                    "###B#C#B#D###",
                    "  #A#D#C#A#",
                    "  #########",
                )
            )
        )
        == initial
    )
    one = State(40, "...B.......", ("BA", "CD", "C", "DA"), 2)
    assert initial.distance(0, 0) == 3
    assert initial.distance(1, 9) == 6
    assert initial.distance(1, 2) == -1
    assert one.distance(1, 1) == -1
    assert one.distance(2, 7) == 3
    assert one in initial.valid_moves()
    assert not one.is_ready(0)
    assert not one.is_ready(1)
    assert one.is_ready(2)
    assert not one.is_ready(3)

    two = State(240, "...B.C.....", ("BA", "D", "C", "DA"), 2)
    assert two in one.valid_moves()
    three = State(440, "...B.......", ("BA", "D", "CC", "DA"), 2)
    assert three in two.valid_moves()
    ten = State(8513, ".....D...A.", ("A", "BB", "CC", "D"), 2)
    eleven = State(12513, ".........A.", ("A", "BB", "CC", "DD"), 2)
    assert eleven in ten.valid_moves()
    solution = State(12521, "...........", ("AA", "BB", "CC", "DD"), 2)
    assert solution in eleven.valid_moves()
    assert not initial.is_solved()
    assert not one.is_solved()
    assert solution.is_solved()
    assert initial.solve() == solution


def test_part2() -> None:
    """
    Examples for Part 2.
    """
    initial = State(0, "...........", ("BDDA", "CCBD", "BBAC", "DACA"), 4)
    assert (
        State.from_input(
            "\n".join(
                (
                    "#############",
                    "#...........#",
                    "###B#C#B#D###",
                    "  #A#D#C#A#",
                    "  #########",
                )
            ),
            True,
        )
        == initial
    )
    assert initial.solve().energy == 44169


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2021, day=23)

    part1 = State.from_input(data)
    print(f"Part 1: {part1.solve().energy}")
    part2 = State.from_input(data, True)
    print(f"Part 2: {part2.solve().energy}")


if __name__ == "__main__":
    main()
