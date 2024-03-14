import os
from PIL import Image

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

    latex_table = "\\begin{tabular}{" + " | ".join(["c"] * num_columns) + "}\n"
    latex_table += "\\hline\n"

    for row in data:
        latex_table += format_row(row) + "\n"

    latex_table += "\\hline\n"
    latex_table += "\\end{tabular}\n"

    return latex_table


def generate_latex_with_image(data, image_path, image_caption="Picture", label="fig:enter-label"):
    latex_table = generate_latex_table(data)

    # Save the image to a separate file
    image_save_path = os.path.join("artifacts", "image.png")
    with Image.open(image_path) as img:
        img.save(image_save_path, format="PNG")

    # Create LaTeX code with the correct image file reference
    latex_code = (
        "\\documentclass{article}\n"
        "\\usepackage{graphicx}\n"
        "\\graphicspath{ {./images/} }\n"
        "\\begin{document}\n"
        f"{latex_table}\n"
        "\\begin{figure}\n"
        "\\centering\n"
        f"\\includegraphics[width=0.5\\linewidth]{{artifacts/image.png}}\n"
        f"\\caption{{{image_caption}}}\n"
        f"\\label{{{label}}}\n"
        "\\end{figure}\n"
        "\\end{document}\n"
    )

    return latex_code