from hw_2.tex_generator import generate_latex_image, generate_latex_table
table_list = [
    ["Header 1", "Header 2", "Header 3"],
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

latex = generate_latex_table(table_list)
latex_with_table = generate_latex_image(latex)

with open("artifacts/2_2_table_image.tex", "w") as tex_file:
    tex_file.write(latex_with_table)

