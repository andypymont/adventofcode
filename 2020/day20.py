"""
2020 Day 20
https://adventofcode.com/2020/day/20
"""

from collections import Counter, deque
from math import sqrt
from itertools import combinations
from typing import Dict, List, Optional, Sequence, Set, Tuple
import aocd  # type: ignore
import numpy as np
import regex as re  # type: ignore

RE_TITLE = re.compile(r"Tile (\d+)")
RE_ROW = re.compile(r"([#\.]+)")


def read_tiles(text: str) -> Dict[int, np.ndarray]:
    tiles = {}
    for tiletext in text.split("\n\n"):
        titlematch = RE_TITLE.search(tiletext)
        rowmatches = RE_ROW.findall(tiletext)
        if titlematch and rowmatches:
            number = int(titlematch.group(1))
            tile = np.array(
                [[1 if char == "#" else 0 for char in row] for row in rowmatches]
            )
            tiles[number] = tile
    return tiles


def edge_matches(edge: np.ndarray, other_tile: np.ndarray) -> bool:
    for other_edge in (
        other_tile[0],
        other_tile[:, -1],
        other_tile[:, 0],
        other_tile[-1],
    ):
        if (edge == other_edge).all():
            return True
        if (np.flip(edge) == other_edge).all():
            return True
    return False


def edges_match(first: np.ndarray, second: np.ndarray) -> bool:
    return any(
        edge_matches(edge, second)
        for edge in (first[0], first[:, -1], first[:, 0], first[-1])
    )


def all_matching_edges(tiles: Dict[int, np.ndarray]) -> Set[Tuple[int, int]]:
    return {
        (first, second)
        for first, second in combinations(tiles.keys(), 2)
        if edges_match(tiles[first], tiles[second])
    }


def find_correct_layout(
    tiles: Dict[int, np.ndarray], matching_edges: Set[Tuple[int, int]]
) -> Sequence[int]:
    grid_size = int(sqrt(len(tiles)))
    tile_neighbours = Counter(
        [first for first, second in matching_edges]
        + [second for first, second in matching_edges]
    )
    search: deque[List[int]] = deque()
    search.append([next(tile for tile, qty in tile_neighbours.items() if qty == 2)])

    while search:
        placed = search.pop()
        position = len(placed)

        if position == len(tiles):
            return placed

        above = position - grid_size if position >= grid_size else None
        left = position - 1 if position % grid_size > 0 else None
        right = position + 1 if position % grid_size < (grid_size - 1) else None
        below = position + grid_size if position + grid_size < len(tiles) else None
        neighbours = sum(1 for adj in (above, left, right, below) if adj is not None)

        not_yet_placed = {
            tile
            for tile in tiles.keys()
            if tile not in placed and tile_neighbours[tile] == neighbours
        }

        for tile in not_yet_placed:
            placeable = True
            if above and not (
                (tile, placed[above]) in matching_edges
                or (placed[above], tile) in matching_edges
            ):
                placeable = False
            if left and not (
                (tile, placed[left]) in matching_edges
                or (placed[left], tile) in matching_edges
            ):
                placeable = False
            if placeable:
                search.append(placed + [tile])

    raise ValueError


def tile_fits(
    tile: np.ndarray,
    above: Optional[np.ndarray],
    below: Optional[np.ndarray],
    left: Optional[np.ndarray],
    right: Optional[np.ndarray],
) -> bool:
    return all(
        (
            above is None or edge_matches(tile[0], above),
            below is None or edge_matches(tile[-1], below),
            left is None or edge_matches(tile[:, 0], left),
            right is None or edge_matches(tile[:, -1], right),
        )
    )


def transformed_to_fit(
    tile: np.ndarray,
    above: Optional[np.ndarray],
    below: Optional[np.ndarray],
    left: Optional[np.ndarray],
    right: Optional[np.ndarray],
) -> np.ndarray:
    for rotations in range(4):
        for hflip in (False, True):
            for vflip in (False, True):
                transformed = np.rot90(tile, rotations)
                if hflip:
                    transformed = np.fliplr(transformed)
                if vflip:
                    transformed = np.flipud(transformed)
                if tile_fits(transformed, above, below, left, right):
                    return transformed
    return tile


def make_image(tiles: Dict[int, np.ndarray], layout: Sequence[int]) -> np.ndarray:
    grid_size = int(sqrt(len(layout)))
    parts = [tiles[tile] for tile in layout]

    # orient tiles to match their required neighbours in the layout
    for row in range(grid_size):
        for col in range(grid_size):
            current = (row * grid_size) + col
            above = parts[current - grid_size] if current >= grid_size else None
            below = (
                parts[current + grid_size]
                if current + grid_size < len(layout)
                else None
            )
            left = parts[current - 1] if current % grid_size > 0 else None
            right = parts[current + 1] if (current + 1) % grid_size != 0 else None
            parts[current] = transformed_to_fit(
                parts[current], above, below, left, right
            )

    # trim the outer elements from each tile
    parts = [tile[1:-1, 1:-1] for tile in parts]

    # combine arrays into a single large array
    return np.concatenate(
        [
            np.concatenate(parts[y * grid_size : (y + 1) * grid_size], axis=1)
            for y in range(grid_size)
        ]
    )


SEA_MONSTER = np.array(
    [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1],
        [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
    ]
)


def count_sea_monsters(image: np.ndarray) -> int:
    monsters = 0
    rows, cols = image.shape
    monsterheight, monsterwidth = SEA_MONSTER.shape

    combos = [
        (rotations, fliph, flipv)
        for rotations in range(3)
        for fliph in (False, True)
        for flipv in (False, True)
    ]
    for rotations, fliph, flipv in combos:
        adjusted_image = np.rot90(image, rotations)
        if fliph:
            adjusted_image = np.fliplr(adjusted_image)
        if flipv:
            adjusted_image = np.flipud(adjusted_image)

        for row in range(rows - monsterheight):
            for col in range(cols - monsterwidth):
                window = adjusted_image[
                    row : row + monsterheight, col : col + monsterwidth
                ]
                if np.greater_equal(window, SEA_MONSTER).all():
                    monsters += 1

    return monsters


def sea_roughness(image: np.ndarray) -> int:
    monsters = count_sea_monsters(image)
    return image.sum() - (SEA_MONSTER.sum() * monsters)


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2020, day=20)

    tiles = read_tiles(data)
    matching_edges = all_matching_edges(tiles)
    layout = find_correct_layout(tiles, matching_edges)

    part1 = layout[0] * layout[11] * layout[132] * layout[143]
    print(f"Part 1: {part1}")

    image = make_image(tiles, layout)
    part2 = sea_roughness(image)
    print(f"Part 2: {part2}")


if __name__ == "__main__":
    main()
