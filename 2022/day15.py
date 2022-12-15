"""
2022 Day 15
https://adventofcode.com/2022/day/15
"""

from dataclasses import dataclass
from typing import Sequence
import re
import aocd  # type: ignore


@dataclass(frozen=True, order=True)
class Point:
    """
    A single point in two-dimensional space.
    """

    y_coord: int
    x_coord: int

    def __sub__(self, other: "Point") -> int:
        """
        Subtracting one Point from another returns the manhattan distance between the two.
        """
        return abs(self.y_coord - other.y_coord) + abs(self.x_coord - other.x_coord)


re_sensor = re.compile(
    r"Sensor at x=([-\d]+), y=([-\d]+): closest beacon is at x=([-\d]+), y=([-\d]+)"
)


@dataclass(frozen=True)
class Sensor:
    """
    A single sensor, consiting of its position and the position of the closest beacon to it.
    """

    sensor: Point
    beacon: Point

    @property
    def beacon_distance(self) -> int:
        """
        Return in the integer manhattan distance between this sensor and its known closest beacon.
        """
        return self.beacon - self.sensor

    @classmethod
    def from_text(cls, text: str) -> "Sensor":
        """
        Read a Sensor from a single line of the puzzle input.
        """
        if match := re_sensor.match(text):
            sensor_x, sensor_y, beacon_x, beacon_y = [int(n) for n in match.groups()]
            return cls(Point(sensor_y, sensor_x), Point(beacon_y, beacon_x))

        raise ValueError(f"Expected string not found in input {repr(text)}")

    def covered_range_for_row(self, y_coord: int) -> range:
        """
        For a given row (y coordinate), return the range of x coordinate values which have been
        scanned by this sensor (i.e. all those as close or closer than its known closest beacon).

        If the row is too far away from this sensor for any impossible-beacon locations to be
        known, the start and stop values of the range will be identical, i.e. it will contain no
        values.
        """
        distance = self.beacon_distance - abs(self.sensor.y_coord - y_coord)
        if distance < 0:
            x_coord = self.sensor.x_coord
            return range(x_coord, x_coord)

        return range(
            self.sensor.x_coord - distance,
            self.sensor.x_coord + distance + 1,
        )


def count_non_beacon_locations_in_row(sensors: Sequence[Sensor], row: int) -> int:
    """
    Return the integer count of all confirmed non-beacon locations in the given row number, based
    on the existence of the given set of sensors.
    """
    ranges = sorted(
        (sensor.covered_range_for_row(row) for sensor in sensors),
        key=lambda r: (r.start, r.stop),
    )

    count = 0
    x_pos = ranges[0].start

    for rng in ranges:
        # if we are already beyond the range (because it was fully overlapped by a previous one),
        # skip it
        if rng.stop <= x_pos:
            continue

        # skip any empty space between the previous x position and this range
        if rng.start > x_pos:
            x_pos = rng.start

        # add values from the current position up until the end of the range and then move to the
        # end of the range
        count += rng.stop - x_pos
        x_pos = rng.stop

    beacons_in_row = {
        sensor.beacon.x_coord for sensor in sensors if sensor.beacon.y_coord == row
    }
    return count - len(beacons_in_row)


def test_part1() -> None:
    """
    Examples for Part 1.
    """
    assert Point(4, 5) - Point(13, 7) == 11
    assert Point(1, 1) - Point(-2, 2) == 4
    assert Point(-12, -15) - Point(-12, -15) == 0
    assert Sensor.from_text(
        "Sensor at x=2, y=18: closest beacon is at x=-2, y=15"
    ) == Sensor(Point(18, 2), Point(15, -2))
    assert Sensor.from_text(
        "Sensor at x=9, y=16: closest beacon is at x=10, y=16"
    ) == Sensor(Point(16, 9), Point(16, 10))
    assert Sensor(Point(18, 2), Point(15, -2)).beacon_distance == 7
    assert Sensor(Point(16, 9), Point(16, 10)).beacon_distance == 1

    assert Sensor(Point(16, 9), Point(16, 10)).covered_range_for_row(16) == range(8, 11)
    assert Sensor(Point(18, 2), Point(15, -2)).covered_range_for_row(18) == range(
        -5, 10
    )
    assert Sensor(Point(18, 2), Point(15, -2)).covered_range_for_row(17) == range(-4, 9)
    assert Sensor(Point(18, 2), Point(15, -2)).covered_range_for_row(16) == range(-3, 8)
    assert Sensor(Point(18, 2), Point(15, -2)).covered_range_for_row(15) == range(-2, 7)
    assert Sensor(Point(18, 2), Point(15, -2)).covered_range_for_row(14) == range(-1, 6)
    assert Sensor(Point(18, 2), Point(15, -2)).covered_range_for_row(13) == range(0, 5)
    assert Sensor(Point(18, 2), Point(15, -2)).covered_range_for_row(12) == range(1, 4)
    assert Sensor(Point(18, 2), Point(15, -2)).covered_range_for_row(11) == range(2, 3)
    assert Sensor(Point(18, 2), Point(15, -2)).covered_range_for_row(10) == range(2, 2)

    sensors = (
        Sensor(Point(18, 2), Point(15, -2)),
        Sensor(Point(16, 9), Point(16, 10)),
        Sensor(Point(2, 13), Point(3, 15)),
        Sensor(Point(14, 12), Point(16, 10)),
        Sensor(Point(20, 10), Point(16, 10)),
        Sensor(Point(17, 14), Point(16, 10)),
        Sensor(Point(7, 8), Point(10, 2)),
        Sensor(Point(0, 2), Point(10, 2)),
        Sensor(Point(11, 0), Point(10, 2)),
        Sensor(Point(14, 20), Point(17, 25)),
        Sensor(Point(20, 17), Point(22, 21)),
        Sensor(Point(7, 16), Point(3, 15)),
        Sensor(Point(3, 14), Point(3, 15)),
        Sensor(Point(1, 20), Point(3, 15)),
    )
    assert count_non_beacon_locations_in_row(sensors, 10) == 26


# def test_part2() -> None:
#     """
#     Examples for Part 2.
#     """
#     assert False


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2022, day=15)
    sensors = tuple(Sensor.from_text(line) for line in data.splitlines())

    print(f"Part 1: {count_non_beacon_locations_in_row(sensors, 2_000_000)}")
    # print(f'Part 2: {p2}')


if __name__ == "__main__":
    main()
