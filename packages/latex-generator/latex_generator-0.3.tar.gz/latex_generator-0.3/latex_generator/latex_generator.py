# latex_generator/latex_generator.py
import base64
from PIL import Image
from io import BytesIO

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


def generate_latex_with_image(data, image_path):
    latex_table = generate_latex_table(data)

    # Подготовка изображения для вставки в LaTeX
    with Image.open(image_path) as img:
        img_buffer = BytesIO()
        img.save(img_buffer, format="PNG")
        img_data = img_buffer.getvalue()

    img_base64 = base64.b64encode(img_data).decode("utf-8")

    # Вставка изображения в LaTeX
    latex_code = (
            "\\documentclass{article}\n"
            "\\usepackage{graphicx}\n"
            "\\begin{document}\n"
            f"{latex_table}\n"
            "\\includegraphics[width=0.5\\textwidth]{{data:image/png;base64," + f"{img_base64}}}\n"
                                                                                "\\end{document}"
    )

    return latex_code