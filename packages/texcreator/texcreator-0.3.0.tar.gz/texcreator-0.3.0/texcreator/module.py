def generate_latex(data):
    header = data[0]
    rows = data[1:]


    latex_document = r"""
\documentclass{article}
\usepackage{fontspec}
\usepackage{polyglossia}
\usepackage{graphicx} % Include the graphicx package

\setmainlanguage{russian}
\setotherlanguages{english}

\setmainfont{Liberation Serif}
\setsansfont{Arial}
\setmonofont{Courier New}

\begin{document}"""

    latex_document += r"""
\begin{table}[h]
\centering
\begin{tabular}{|""" + "l|" * len(header) + "}\n\\hline\n"

    latex_document += " & ".join(header) + r" \\\hline" + "\n"

    for row in rows:
        latex_document += " & ".join(row) + r" \\\hline" + "\n"

    latex_document += r"""
\end{tabular}
\end{table}
"""

    return latex_document


def insert_image(latex_file_path, image_path, caption="Image", label="fig:image"):
    image_latex_code = f"""
\\begin{{figure}}[h]
    \\centering
    \\includegraphics[width=0.9\\textwidth]{{{image_path}}}
    \\caption{{{caption}}}
    \\label{{{label}}}
\\end{{figure}}
\\end{document}
"""
    with open(latex_file_path, 'a') as file:
        file.write(image_latex_code)


