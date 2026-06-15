"""Remainder Report Generator.

Reads a list of dividend values and a list of divisor values from two input
text files, computes the remainder (dividend % divisor) for every
dividend/divisor combination, and writes a plain-text report listing the
results for each dividend.

Input files may contain numbers separated by whitespace, commas, and/or
newlines (e.g. "10, 23.5\n7"); any token that cannot be parsed as a number is
skipped.

Usage:
    python remainder_report.py [dividends_file] [divisors_file] [output_file]

All three arguments are optional and default to:
    dividends_file = "dividends.txt"
    divisors_file  = "divisors.txt"
    output_file    = "remainders.txt"

Example output:
    For the number 10.0, the remainders are: 1.0, 2.0, undefined (division by zero), 0.0
    For the number 23.0, the remainders are: 2.0, 3.0, undefined (division by zero), 3.0
"""

from __future__ import annotations

import argparse
from pathlib import Path


def read_numbers(filepath: str | Path) -> list[float]:
    """Read every numeric token from a text file into a list of floats.

    Commas are treated as separators alongside whitespace, and any token
    that cannot be parsed as a float is skipped.
    """
    numbers: list[float] = []
    with open(filepath, "r") as f:
        for line in f:
            for token in line.replace(",", " ").split():
                try:
                    numbers.append(float(token))
                except ValueError:
                    continue
    return numbers


def build_remainder_report(
    dividends: list[float], divisors: list[float], precision: int = 4
) -> str:
    """Build a text report of ``dividend % divisor`` for every combination.

    Each dividend gets one line listing the remainder produced by every
    divisor, in the same order as ``divisors``. A divisor of zero is
    reported as undefined rather than raising ``ZeroDivisionError``.
    """
    lines: list[str] = []
    for dividend in dividends:
        remainders = []
        for divisor in divisors:
            if divisor == 0:
                remainders.append("undefined (division by zero)")
            else:
                remainders.append(str(round(dividend % divisor, precision)))
        lines.append(
            f"For the number {dividend}, the remainders are: " + ", ".join(remainders)
        )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "dividends_file", nargs="?", default="dividends.txt",
        help="File containing dividend values (default: dividends.txt)",
    )
    parser.add_argument(
        "divisors_file", nargs="?", default="divisors.txt",
        help="File containing divisor values (default: divisors.txt)",
    )
    parser.add_argument(
        "output_file", nargs="?", default="remainders.txt",
        help="File to write the report to (default: remainders.txt)",
    )
    args = parser.parse_args()

    dividends = read_numbers(args.dividends_file)
    divisors = read_numbers(args.divisors_file)

    report = build_remainder_report(dividends, divisors)

    with open(args.output_file, "w") as f:
        f.write(report)

    print(f"Processed {len(dividends)} dividend(s) and {len(divisors)} divisor(s).")
    print(f"Report written to {args.output_file}")


if __name__ == "__main__":
    main()
