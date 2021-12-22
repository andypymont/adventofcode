"""
2021 Day 19
https://adventofcode.com/2021/day/19
"""

from itertools import combinations
from typing import Dict, Iterable, List, Set, Tuple
import aocd  # type: ignore
import numpy as np


def read_scanner(lines: Iterable[str]) -> np.ndarray:
    return np.array([[int(val) for val in line.split(",")] for line in lines])


def read_scanners(text: str) -> Dict[int, np.ndarray]:
    scanners: Dict[int, np.ndarray] = {}
    for scanner in text.split("\n\n"):
        lines = scanner.split("\n")
        scanners[int(lines[0][12:-4])] = read_scanner(lines[1:])
    return scanners


FLIPS = {(x, y, z) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)}
ROTATIONS = {(0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)}


def all_orientations(scanner: np.ndarray) -> List[np.ndarray]:
    return [scanner[:, rotate] * flip for rotate in ROTATIONS for flip in FLIPS]


def common_point_count(first: np.ndarray, second: np.ndarray) -> int:
    return int(first[(first[:, None] == second).all(-1).any(1)].shape[0])


def overlap(first: np.ndarray, second: np.ndarray) -> Tuple[int, np.ndarray]:
    """
    Find the overlap between two scanners by moving the second in three dimensions to match with
    the first. Return value is a tuple (quantity: int, offset: np.ndarray) representing the highest
    number of achievable overlapping points, and the an array representing the offset to each point
    needed to achieve this.
    """
    return max(
        [
            (common_point_count(first, sec), offset)
            for sec, offset in [
                (second + offset, offset)
                for offset in [pt1 - pt2 for pt1 in first for pt2 in second]
            ]
        ],
        key=lambda item: item[0],
    )


def best_overlap(
    first: np.ndarray, second: np.ndarray
) -> Tuple[int, np.ndarray, np.ndarray]:
    """
    Find the best overlap between two scanners by rotating and moving the second to match with the
    first (which remains static). Return value is a tuple:
    (quantity: int, offset: np.ndarray, modified: np.ndarray)
    Where quantity is the highest number of achievable overlapping points, offset is the movement
    needed within the coordinate set relevant to first, and modified is a version of second
    realigned to first's coordinate system.
    """
    return max(
        [
            (over[0], over[1], orient + over[1])
            for over, orient in [
                (overlap(first, orient), orient) for orient in all_orientations(second)
            ]
        ],
        key=lambda item: item[0],
    )


def build_overlap_map(scanners: Dict[int, np.ndarray]) -> Dict[int, Set[int]]:
    """
    Evaluate the provided set of scanners and return a mapping of each scanner number to the set of
    scanner numbers with which it overlaps >= 12.
    """
    overlap_map: Dict[int, Set[int]] = {}
    for first, second in combinations(scanners, 2):
        if first not in overlap_map:
            overlap_map[first] = set()
        if second not in overlap_map:
            overlap_map[second] = set()
        over, _, _ = best_overlap(scanners[first], scanners[second])
        if over >= 12:
            overlap_map[first].add(second)
            overlap_map[second].add(first)
    return overlap_map


def hashable_point(point: np.ndarray) -> str:
    return f"{point[0]},{point[1]},{point[2]}"


def normalise_scanners(
    scanners: Dict[int, np.ndarray], overlap_map: Dict[int, Set[int]]
) -> Tuple[Dict[int, np.ndarray], Set[str]]:
    """
    Create the map of scanners aligned to the coordinate map of scanner[0]. Return value is a tuple
    (locations: Dict[int, np.ndarray], beacons: Set[str]) where locations is a mapping of scanner
    number to its location in the coordinate system and beacons is the set of distinct beacons
    visible to the scanner collection.
    """
    locations: Dict[int, np.ndarray] = {0: np.array([0, 0, 0])}
    transformed: Dict[int, np.ndarray] = {0: scanners[0]}
    beacons: Set[str] = set(hashable_point(pt) for pt in scanners[0])

    while len(locations) < len(scanners):
        for existing in tuple(locations):
            reachable_unmapped = {
                s for s in overlap_map[existing] if s not in locations
            }
            for scanner in reachable_unmapped:
                _, offset, new_beacons = best_overlap(
                    transformed[existing], scanners[scanner]
                )
                locations[scanner] = offset
                transformed[scanner] = new_beacons
                beacons.update(hashable_point(pt) for pt in new_beacons)

    return locations, beacons


def manhattan_distance(first: np.ndarray, second: np.ndarray) -> int:
    return sum(abs(first[dim] - second[dim]) for dim in range(3))


def largest_manhattan_distance(locations: Dict[int, np.ndarray]) -> int:
    return max(
        manhattan_distance(first, second)
        for first, second in combinations(locations.values(), 2)
    )


def test_parts1and2() -> None:
    """
    Examples for Part 1.
    """
    scanners = read_scanners(
        "\n".join(
            (
                "--- scanner 0 ---",
                "404,-588,-901",
                "528,-643,409",
                "-838,591,734",
                "390,-675,-793",
                "-537,-823,-458",
                "-485,-357,347",
                "-345,-311,381",
                "-661,-816,-575",
                "-876,649,763",
                "-618,-824,-621",
                "553,345,-567",
                "474,580,667",
                "-447,-329,318",
                "-584,868,-557",
                "544,-627,-890",
                "564,392,-477",
                "455,729,728",
                "-892,524,684",
                "-689,845,-530",
                "423,-701,434",
                "7,-33,-71",
                "630,319,-379",
                "443,580,662",
                "-789,900,-551",
                "459,-707,401",
                "",
                "--- scanner 1 ---",
                "686,422,578",
                "605,423,415",
                "515,917,-361",
                "-336,658,858",
                "95,138,22",
                "-476,619,847",
                "-340,-569,-846",
                "567,-361,727",
                "-460,603,-452",
                "669,-402,600",
                "729,430,532",
                "-500,-761,534",
                "-322,571,750",
                "-466,-666,-811",
                "-429,-592,574",
                "-355,545,-477",
                "703,-491,-529",
                "-328,-685,520",
                "413,935,-424",
                "-391,539,-444",
                "586,-435,557",
                "-364,-763,-893",
                "807,-499,-711",
                "755,-354,-619",
                "553,889,-390",
                "",
                "--- scanner 2 ---",
                "649,640,665",
                "682,-795,504",
                "-784,533,-524",
                "-644,584,-595",
                "-588,-843,648",
                "-30,6,44",
                "-674,560,763",
                "500,723,-460",
                "609,671,-379",
                "-555,-800,653",
                "-675,-892,-343",
                "697,-426,-610",
                "578,704,681",
                "493,664,-388",
                "-671,-858,530",
                "-667,343,800",
                "571,-461,-707",
                "-138,-166,112",
                "-889,563,-600",
                "646,-828,498",
                "640,759,510",
                "-630,509,768",
                "-681,-892,-333",
                "673,-379,-804",
                "-742,-814,-386",
                "577,-820,562",
                "",
                "--- scanner 3 ---",
                "-589,542,597",
                "605,-692,669",
                "-500,565,-823",
                "-660,373,557",
                "-458,-679,-417",
                "-488,449,543",
                "-626,468,-788",
                "338,-750,-386",
                "528,-832,-391",
                "562,-778,733",
                "-938,-730,414",
                "543,643,-506",
                "-524,371,-870",
                "407,773,750",
                "-104,29,83",
                "378,-903,-323",
                "-778,-728,485",
                "426,699,580",
                "-438,-605,-362",
                "-469,-447,-387",
                "509,732,623",
                "647,635,-688",
                "-868,-804,481",
                "614,-800,639",
                "595,780,-596",
                "",
                "--- scanner 4 ---",
                "727,592,562",
                "-293,-554,779",
                "441,611,-461",
                "-714,465,-776",
                "-743,427,-804",
                "-660,-479,-426",
                "832,-632,460",
                "927,-485,-438",
                "408,393,-506",
                "466,436,-512",
                "110,16,151",
                "-258,-428,682",
                "-393,719,612",
                "-211,-452,876",
                "808,-476,-593",
                "-575,615,604",
                "-485,667,467",
                "-680,325,-822",
                "-627,-443,-432",
                "872,-547,-609",
                "833,512,582",
                "807,604,487",
                "839,-516,451",
                "891,-625,532",
                "-652,-548,-490",
                "30,-46,-14",
            )
        )
    )
    assert len(scanners) == 5
    assert scanners.keys() == {0, 1, 2, 3, 4}
    assert (
        scanners[0]
        == np.array(
            [
                [404, -588, -901],
                [528, -643, 409],
                [-838, 591, 734],
                [390, -675, -793],
                [-537, -823, -458],
                [-485, -357, 347],
                [-345, -311, 381],
                [-661, -816, -575],
                [-876, 649, 763],
                [-618, -824, -621],
                [553, 345, -567],
                [474, 580, 667],
                [-447, -329, 318],
                [-584, 868, -557],
                [544, -627, -890],
                [564, 392, -477],
                [455, 729, 728],
                [-892, 524, 684],
                [-689, 845, -530],
                [423, -701, 434],
                [7, -33, -71],
                [630, 319, -379],
                [443, 580, 662],
                [-789, 900, -551],
                [459, -707, 401],
            ]
        )
    ).all()
    assert best_overlap(scanners[0], scanners[1])[0] == 12
    overlap_map = build_overlap_map(scanners)
    locations, beacons = normalise_scanners(scanners, overlap_map)
    assert (locations[0] == np.array([0, 0, 0])).all()
    assert (locations[1] == np.array([68, -1246, -43])).all()
    assert (locations[4] == np.array([-20, -1133, 1061])).all()
    assert len(beacons) == 79
    assert largest_manhattan_distance(locations) == 3621


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2021, day=19)
    scanners = read_scanners(data)
    overlap_map = build_overlap_map(scanners)
    locations, beacons = normalise_scanners(scanners, overlap_map)

    print(f"Part 1: {len(beacons)}")
    print(f"Part 2: {largest_manhattan_distance(locations)}")


if __name__ == "__main__":
    main()
