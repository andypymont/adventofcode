"""
2016 Day 5
https://adventofcode.com/2016/day/5
"""

from functools import lru_cache
from hashlib import md5
import aocd  # type: ignore


@lru_cache
def md5hash(door: str, index: int) -> str:
    """
    Calculate the md5 hash for the given Door ID and integer index.
    """
    return md5((door + str(index)).encode("utf-8")).hexdigest()


def create_password(door: str) -> str:
    """
    Create a password for the given door - i.e. the sixth character of each of the first eight
    hashes beginning with five 0s.
    """
    password = ""
    index = 0
    while len(password) < 8:
        hsh = md5hash(door, index)
        if hsh[:5] == "00000":
            password += hsh[5]
        index += 1
    return password


def create_password2(door: str) -> str:
    """
    Create the password using the part 2 algorithm.
    """
    password: list[str] = ["z", "z", "z", "z", "z", "z", "z", "z"]
    index = 0
    while any(digit == "z" for digit in password) > 0:
        hsh = md5hash(door, index)
        if hsh[:5] == "00000":
            try:
                digit = int(hsh[5])
            except ValueError:
                digit = 8
            if digit <= 7 and password[digit] == "z":
                password[digit] = hsh[6]
        index += 1
    return "".join(password)


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2016, day=5)

    print(f"Part 1: {create_password(data)}")
    print(f"Part 2: {create_password2(data)}")


if __name__ == "__main__":
    main()
