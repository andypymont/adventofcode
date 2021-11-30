"""
2018 Day 10
https://adventofcode.com/2018/day/10
"""

import re
import aocd # type: ignore
import pandas as pd # type: ignore

re_point = re.compile(r'position=<([- \d]+), ([- \d]+)> velocity=<([- \d]+), ([- \d]+)>')

def dataframe_from_input(text: str) -> pd.DataFrame:
    points = [map(int, point) for point in re_point.findall(text)]
    return pd.DataFrame(points, columns=('x', 'y', 'vx', 'vy'), dtype='int64')

def valuerange(series: pd.Series) -> int:
    return series.max() - series.min()

def y_values_after_seconds(dataframe: pd.DataFrame, seconds: int) -> pd.Series:
    return dataframe['vy'] * seconds + dataframe['y']

def x_values_after_seconds(dataframe: pd.DataFrame, seconds: int) -> pd.Series:
    return dataframe['vx'] * seconds + dataframe['x']

def find_message_second(dataframe: pd.DataFrame) -> int:
    second = 0
    y_height = valuerange(dataframe['y'])

    while True:
        second += 1
        new_y_height = valuerange(y_values_after_seconds(dataframe, second))
        if new_y_height > y_height:
            return second - 1
        y_height = new_y_height

def print_message(dataframe: pd.DataFrame, seconds: int) -> str:
    x_values = x_values_after_seconds(dataframe, seconds)
    y_values = y_values_after_seconds(dataframe, seconds)
    points = set(zip(x_values, y_values))

    return '\n'.join(
        ''.join('#' if (x, y) in points else ' ' for x in range(x_values.min(), x_values.max()+1))
        for y in range(y_values.min(), y_values.max()+1)
    )

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2018, day=10)

    points = dataframe_from_input(data)
    part2 = find_message_second(points)
    part1 = print_message(points, part2)
    print(f'Part 1: \n{part1}')
    print(f'Part 2: {part2}')

if __name__ == '__main__':
    main()
