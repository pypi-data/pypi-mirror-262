def image_to_latex_document(image_path):
    latex_document = "\\documentclass{article}\n"
    latex_document += "\\usepackage{graphicx}\n"
    latex_document += "\\begin{document}\n\n"

    # Adding the image
    latex_document += "\\begin{figure}[h!]\n\\centering\n"
    latex_document += "\\includegraphics[width=0.5\\textwidth]{" + image_path + "}\n"
    latex_document += "\\end{figure}\n"  # Close the figure environment

    latex_document += "\\end{document}"

    return latex_document