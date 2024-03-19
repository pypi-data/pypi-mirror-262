def list_of_lists_to_latex_document(data):
    latex_document = "\\documentclass{article}\n"
    latex_document += "\\begin{document}\n\n"
    latex_document += "\\begin{table}[h!]\n\\centering\n\\begin{tabular}{|" + "c|" * len(data[0]) + "}\n\\hline\n"

    for row in data:
        latex_document += " & ".join(str(cell) for cell in row)
        latex_document += " \\\\\n\\hline\n"

    latex_document += "\\end{tabular}\n"
    latex_document += "\\end{table}\n\n"
    latex_document += "\\end{document}"

    return latex_document