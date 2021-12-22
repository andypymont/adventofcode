"""
2016 Day 4
https://adventofcode.com/2016/day/4
"""

from dataclasses import dataclass
from typing import Dict
import string
import aocd  # type: ignore


@dataclass(frozen=True)
class Room:
    """
    A room as per the puzzle input; the base data-class properties are those from the input whilst
    the calculated properties allow for the true attributes to be calculated.
    """

    name: str
    sector_id: int
    checksum: str

    @classmethod
    def from_input_line(cls, line: str) -> "Room":
        """
        Create an instance from a single line of the puzzle input.
        """
        parts = line.split("-")
        words, data = parts[:-1], parts[-1].split("[")
        return cls(name="-".join(words), sector_id=int(data[0]), checksum=data[1][:-1])

    @property
    def name_histogram(self) -> Dict[str, int]:
        """
        Count the letters in the name of the room and return a mapping of how many times each
        appears.
        """
        return {
            letter: sum(1 for let in self.name.lower() if let == letter)
            for letter in self.name
            if letter in string.ascii_lowercase
        }

    @property
    def actual_checksum(self) -> str:
        """
        Calculate the room's actual check-sum based on its name, rather than the checksum value
        from the puzzle input.
        """
        return "".join(
            letter
            for (letter, count) in sorted(
                self.name_histogram.items(), key=lambda x: (-x[1], x[0])
            )[:5]
        )

    @property
    def is_real(self) -> bool:
        """
        Return whether or not the room is real - i.e. the real checksum matches the one from the
        puzzle input.
        """
        return self.checksum == self.actual_checksum

    def _decrypt_letter(
        self, letter: str, letters: str = string.ascii_lowercase
    ) -> str:
        if letter == "-":
            return " "
        if letter in letters:
            return letters[(letters.index(letter) + self.sector_id) % 26]
        return ""

    @property
    def decrypted_name(self) -> str:
        """
        The true, decrypted name of the room.
        """
        return "".join(self._decrypt_letter(letter) for letter in self.name)


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2016, day=4)
    rooms = [Room.from_input_line(line) for line in data.split("\n")]

    total_sectorids = sum(room.sector_id for room in rooms if room.is_real)
    print(f"Part 1: {total_sectorids}")
    northpole = next(room for room in rooms if "northpole" in room.decrypted_name)
    print(f"Part 2: {northpole.sector_id}")


if __name__ == "__main__":
    main()
