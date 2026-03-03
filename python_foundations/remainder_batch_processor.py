"""
Project: Remainder Batch Processor
Language: Python
Concepts Demonstrated:
- File I/O
- Data parsing and cleaning
- Exception handling
- Modular function design
- Output file generation

Objective:
Read numeric values from two input files,
compute modulo operations between datasets,
and export structured results to a new file.
"""

def extract_numeric_values(filepath):
    """
    Reads a text file and extracts numeric values.
    Non-numeric entries are ignored.
    """
    values = []

    with open(filepath, "r") as file:
        for line in file:
            tokens = line.replace(",", " ").split()

            for token in tokens:
                try:
                    values.append(float(token))
                except ValueError:
                    continue

    return values


def compute_remainders(base_numbers, divisors):
    """
    Computes remainders for each base number
    against a list of divisors.
    """
    output_lines = []

    for base in base_numbers:
        output_lines.append(f"For the number {base}:")

        results = []
        for divisor in divisors:
            try:
                results.append(str(base % divisor))
            except ZeroDivisionError:
                results.append("Divide by 0 encountered")

        output_lines.append(", ".join(results))
        output_lines.append("")

    return output_lines


def write_output(filepath, lines):
    """Writes processed results to output file."""
    with open(filepath, "w") as file:
        file.write("\n".join(lines))


if __name__ == "__main__":
    main_numbers = extract_numeric_values("First.txt")
    divisor_numbers = extract_numeric_values("Second.txt")

    results = compute_remainders(main_numbers, divisor_numbers)
    write_output("Third.txt", results)
