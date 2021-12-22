"""
2016 Day 13
https://adventofcode.com/2016/day/13
"""

from collections import deque
from typing import Dict, Iterator, Tuple
import aocd  # type: ignore

Point = Tuple[int, int]


def is_wall(maze_no: int, x_coord: int, y_coord: int) -> bool:
    """
    Generic wall check for mazes of all numbers.
    """
    checksum = sum(
        (
            x_coord * x_coord,
            3 * x_coord,
            2 * x_coord * y_coord,
            y_coord,
            y_coord * y_coord,
            maze_no,
        )
    )
    return any((x_coord < 0, y_coord < 0, format(checksum, "b").count("1") % 2 == 1))


class Maze:
    """
    A maze as described in the puzzle input.
    """

    compass = ((0, 1), (1, 0), (0, -1), (-1, 0))

    def __init__(self, number: int):
        self.number = number
        self.layout: Dict[Point, bool] = {}

    def is_wall(self, x_coord: int, y_coord: int) -> bool:
        """
        Specific is_wall function for this maze, caching results from the generic is_wall function.
        """
        if (x_coord, y_coord) not in self.layout:
            self.layout[(x_coord, y_coord)] = is_wall(self.number, x_coord, y_coord)
        return self.layout[(x_coord, y_coord)]

    def accessible_neighbours(self, x_coord: int, y_coord: int) -> Iterator[Point]:
        """
        Yield each accessible neighbour from the given location.
        """
        for x_delta, y_delta in self.compass:
            x_new, y_new = x_coord + x_delta, y_coord + y_delta
            if not self.is_wall(x_new, y_new):
                yield (x_new, y_new)

    def shortest_path_between(self, start: Point, finish: Point) -> int:
        """
        Part 1 solver function -- return the length of the shortest path between two points.
        """
        search = deque([(0, start)])
        visited: set[Point] = set()

        while search:
            dist, (x_coord, y_coord) = search.popleft()
            if (x_coord, y_coord) == finish:
                return dist
            if (x_coord, y_coord) not in visited:
                visited.add((x_coord, y_coord))
                search.extend(
                    (dist + 1, (newx, newy))
                    for newx, newy in self.accessible_neighbours(x_coord, y_coord)
                )

        return -1

    def cells_visitable_in_steps(self, start: Point, steps: int) -> int:
        """
        Part 2 solver function -- return the number of distinct cells visitable within the given
        number of steps from the given start location.
        """
        search = deque([(0, start)])
        visited: set[Point] = set()

        while search:
            dist, (x_coord, y_coord) = search.popleft()
            if dist == steps + 1:
                return len(visited)
            if (x_coord, y_coord) not in visited:
                visited.add((x_coord, y_coord))
                search.extend(
                    (dist + 1, (newx, newy))
                    for newx, newy in self.accessible_neighbours(x_coord, y_coord)
                )

        return -1


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2016, day=13)
    maze = Maze(int(data))

    print(f"Part 1: {maze.shortest_path_between((1, 1), (31, 39))}")
    print(f"Part 2: {maze.cells_visitable_in_steps((1, 1), 50)}")


if __name__ == "__main__":
    main()
