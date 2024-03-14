import os


def generate_latex_table(data):
    if not data or not all(isinstance(row, list) for row in data):
        raise ValueError("Input must be a non-empty list of lists")

    num_columns = max(len(row) for row in data)

    def format_cell(cell):
        return str(cell) if cell is not None else ""

    def format_row(row):
        formatted_cells = [format_cell(cell) for cell in row]
        missing_cells = num_columns - len(formatted_cells)
        formatted_cells.extend(["" for _ in range(missing_cells)])
        return " & ".join(formatted_cells) + " \\\\"

    latex_table = "\\documentclass{article}\n"
    latex_table += "\\begin{document}\n"
    latex_table += "\\begin{tabular}{" + " | ".join(["c"] * num_columns) + "}\n"
    latex_table += "\\hline\n"

    for row in data:
        latex_table += format_row(row) + "\n"

    latex_table += "\\hline\n"
    latex_table += "\\end{tabular}\n"
    latex_table += "\\end{document}"

    return latex_table


if __name__ == "__main__":
    example_data = [
        ["Header 1", "Header 2", "Header 3"],
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]

    script_directory = os.path.dirname(os.path.abspath(__file__))
    artifacts_directory = os.path.join(script_directory, "artifacts")
    os.makedirs(artifacts_directory, exist_ok=True)

    latex_code = generate_latex_table(example_data)

    with open(os.path.join(artifacts_directory, "artifact_1.tex"), "w") as file:
        file.write(latex_code)