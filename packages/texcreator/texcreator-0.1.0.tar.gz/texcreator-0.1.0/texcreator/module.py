def generate_latext(data):

    header = data[0]
    rows = data[1:]
    latex_document = r"""
\documentclass{article}
\usepackage{fontspec}
\usepackage{polyglossia}
\setmainlanguage{russian}
\setotherlanguages{english}

\setmainfont{Liberation Serif}
\setsansfont{Arial}
\setmonofont{Courier New}"""
    latex_document += "\\begin{table}[h]\n\\centering\n"
    latex_document += "\\begin{tabular}{|" + \
        "l|" * len(header) + "}\n\\hline\n"

    latex_document += " & ".join(header) + " \\\\\n\\hline\n"

    for row in rows:
        latex_document += " & ".join(row) + " \\\\\n\\hline\n"

    latex_document += "\\end{tabular}\n"
    latex_document += "\\end{table}\n"

    return latex_document

def insert_image(latex_file_path, image_path, caption="Image", label="fig:image"):

    image_latex_code = f"""
\\begin{{figure}}[h]
    \\centering
    \\includegraphics[width=0.9\\textwidth]{{{image_path}}}
    \\caption{{{caption}}}
    \\label{{{label}}}
\\end{{figure}}
"""

    with open(latex_file_path, 'a') as file:
        file.write(image_latex_code)

