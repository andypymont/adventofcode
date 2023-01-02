"""
2022 Day 7
https://adventofcode.com/2022/day/7
"""

from dataclasses import dataclass
from typing import Optional
import aocd  # type: ignore


@dataclass(frozen=True)
class File:
    """
    A single file on the file system, consisting of its location (path without filename), filename,
    and size.
    """

    location: str
    name: str
    size: int


class FileSystem:
    """
    A virtual file system of files and folders, read from the puzzle input.
    """

    DISK_SIZE = 70_000_000
    REQUIRED_SPACE = 30_000_000

    def __init__(self, text: str):
        self.folders = set()
        self.files = set()

        path: tuple[str, ...] = ()
        for line in text.splitlines():
            if line == "$ cd /":
                path = ()
            elif line == "$ cd ..":
                path = path[:-1]
            elif line[:5] == "$ cd ":
                path = path + (line[5:],)
                self.folders.add("/".join(path))
            elif line == "$ ls":
                pass
            elif line[:4] == "dir ":
                self.folders.add("/".join(path + (line[4:],)))
            else:
                parts = line.split(" ")
                self.files.add(File("/".join(path), parts[1], int(parts[0])))

    def size(self, path: str) -> int:
        """
        Return the size of the given folder, i.e. the total of the size of all files within that
        path including all subfolders.
        """
        return sum(file.size for file in self.files if file.location.startswith(path))

    def deletion_candidates(
        self, min_size: int = 0, max_size: Optional[int] = None
    ) -> dict[str, int]:
        """
        Return a dictionary of all deletion candidates (folders with a specified minimum and
        maximum size), mapping their paths to their total size.
        """
        max_size = max_size or self.DISK_SIZE
        return {
            folder: size
            for folder, size in ((folder, self.size(folder)) for folder in self.folders)
            if min_size <= size <= max_size
        }

    def total_small_deletion_candidates(self) -> int:
        """
        Return the total size of all small (size less than 100,000) deletion candidates.
        """
        return sum(self.deletion_candidates(max_size=100_000).values())

    def smallest_viable_deletion_candidate_size(self) -> int:
        """
        Return the size of the smallest deletion candidate which will increase the free space on
        the disk to what is required.
        """
        free_space = self.DISK_SIZE - sum(file.size for file in self.files)
        min_size = self.REQUIRED_SPACE - free_space
        return min(value for value in self.deletion_candidates(min_size).values())


def test_part1() -> None:
    """
    Examples for Part 1.
    """
    example = "\n".join(
        (
            "$ cd /",
            "$ ls",
            "dir a",
            "14848514 b.txt",
            "8504156 c.dat",
            "dir d",
            "$ cd a",
            "$ ls",
            "dir e",
            "29116 f",
            "2557 g",
            "62596 h.lst",
            "$ cd e",
            "$ ls",
            "584 i",
            "$ cd ..",
            "$ cd ..",
            "$ cd d",
            "$ ls",
            "4060174 j",
            "8033020 d.log",
            "5626152 d.ext",
            "7214296 k",
        )
    )

    file_system = FileSystem(example)
    assert file_system.folders == {"a", "a/e", "d"}
    assert file_system.files == {
        File("a/e", "i", 584),
        File("a", "f", 29116),
        File("a", "g", 2557),
        File("a", "h.lst", 62596),
        File("", "b.txt", 14848514),
        File("", "c.dat", 8504156),
        File("d", "j", 4060174),
        File("d", "d.log", 8033020),
        File("d", "d.ext", 5626152),
        File("d", "k", 7214296),
    }

    assert file_system.size("a/e") == 584
    assert file_system.size("a") == 94_853
    assert file_system.size("d") == 24_933_642
    assert file_system.size("") == 48_381_165
    assert file_system.deletion_candidates(max_size=100_000) == {
        "a": 94_853,
        "a/e": 584,
    }
    assert file_system.total_small_deletion_candidates() == 95_437


def test_part2() -> None:
    """
    Examples for Part 2.
    """
    example = "\n".join(
        (
            "$ cd /",
            "$ ls",
            "dir a",
            "14848514 b.txt",
            "8504156 c.dat",
            "dir d",
            "$ cd a",
            "$ ls",
            "dir e",
            "29116 f",
            "2557 g",
            "62596 h.lst",
            "$ cd e",
            "$ ls",
            "584 i",
            "$ cd ..",
            "$ cd ..",
            "$ cd d",
            "$ ls",
            "4060174 j",
            "8033020 d.log",
            "5626152 d.ext",
            "7214296 k",
        )
    )
    file_system = FileSystem(example)

    assert file_system.smallest_viable_deletion_candidate_size() == 24_933_642


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2022, day=7)
    file_system = FileSystem(data)

    print(f"Part 1: {file_system.total_small_deletion_candidates()}")
    print(f"Part 2: {file_system.smallest_viable_deletion_candidate_size()}")


if __name__ == "__main__":
    main()
