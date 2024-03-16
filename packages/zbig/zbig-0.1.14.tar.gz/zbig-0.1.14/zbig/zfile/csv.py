#!/usr/bin/env python3

import csv


def read_csv(file_path: str) -> tuple:
    rows = []
    with open(file_path, "r") as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        rows.extend(iter(csvreader))
    return header, rows


def write_csv_append(file_path: str, row: list):
    if check_duplicate(file_path, row):
        # https://docs.python.org/3/library/exceptions.html#exception-hierarchy
        raise ValueError(f"Duplicate data {row}")
    with open(file_path, "a") as file:
        # 默认是 windows 的换行结束符
        csvwriter = csv.writer(file, lineterminator="\n")
        csvwriter.writerow(row)


def check_duplicate(file_path: str, row: list) -> bool:
    _, rows = read_csv(file_path)
    return any(r == row for r in rows)


if __name__ == "__main__":
    header, rows = read_csv("hosts.csv")
    print(header)
    print(rows)
    for row in rows:
        write_csv_append("hosts.csv", row)
    print("write_csv done")
