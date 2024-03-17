def generate_latex_table(data):
    # Начало таблицы
    latex = "\\begin{table}[h!]\n\\centering\n"
    # Определение количества столбцов
    num_columns = len(data[0])
    # Форматирование столбцов
    latex += "\\begin{tabular}{" + " | ".join(["c"] * num_columns) + " }\n\\hline\n"
    # Добавление данных
    for row in data:
        latex += " & ".join(map(str, row)) + " \\\\\n\\hline\n"
    latex += "\\end{tabular}\n"
    latex += "\\end{table}\n"
    return latex

def generate_latex_image(image_path, caption="Figure", label="fig:my_label"):
    latex = "\\begin{figure}[h!]\n\\centering\n"
    latex += f"\\includegraphics[width=0.7\\textwidth]{{{image_path}}}\n"
    latex += f"\\caption{{{caption}}}\n"
    latex += f"\\label{{{label}}}\n"
    latex += "\\end{figure}\n"
    return latex