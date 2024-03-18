from tex_generator import generate_latex_table

data = [
    ["Header 1", "Header 2", "Header 3"],
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

latex_table = generate_latex_table(data)

with open("artifacts/2_1_table.tex", "w") as tex_file:
    tex_file.write(latex_table)