def create_tex_doc():
    latex = "\\documentclass{article}\n"
    latex += "\\usepackage{graphicx}\n"
    latex += "\\begin{document}\n"

    return latex

def create_end_tex_doc(latex):
    latex += "\\end{document}"
    return latex

def generate_latex_table(data, latex=None):
    if latex is None:
        latex = create_tex_doc()
        # Начало таблицы
        latex += "\\begin{table}[h!]\n\\centering\n"
        # Определение количества столбцов
        num_columns = len(data[0])
        # Форматирование столбцов
        latex += "\\begin{tabular}{" + " | ".join(["c"] * num_columns) + " }\n\\hline\n"
        # Добавление данных
        for row in data:
            latex += " & ".join(map(str, row)) + " \\\\\n\\hline\n"
        latex += "\\end{tabular}\n"
        latex += "\\end{table}\n"
        latex = create_end_tex_doc(latex)
    else:
        latex += "\\begin{table}[h!]\n\\centering\n"
        num_columns = len(data[0])
        latex += "\\begin{tabular}{" + " | ".join(["c"] * num_columns) + " }\n\\hline\n"
        for row in data:
            latex += " & ".join(map(str, row)) + " \\\\\n\\hline\n"
        latex += "\\end{tabular}\n"
        latex += "\\end{table}\n"
        latex = create_end_tex_doc(latex)

    return latex

def generate_latex_image(image_path = 'artifacts/data/cat.png', caption="Figure", label="fig:my_label", latex=None):
    if latex is None:
        latex = create_tex_doc()
        latex += "\\begin{figure}[h!]\n\\centering\n"
        latex += f"\\includegraphics[width=0.7\\textwidth]{{{image_path}}}\n"
        latex += f"\\caption{{{caption}}}\n"
        latex += f"\\label{{{label}}}\n"
        latex += "\\end{figure}\n"
        latex = create_end_tex_doc(latex)
    else:
        latex = latex.replace("\\end{document}", "")
        latex += "\\begin{figure}[h!]\n\\centering\n"
        latex += f"\\includegraphics[width=0.7\\textwidth]{{{image_path}}}\n"
        latex += f"\\caption{{{caption}}}\n"
        latex += f"\\label{{{label}}}\n"
        latex += "\\end{figure}\n"
        latex = create_end_tex_doc(latex)

    return latex
