
def table_generation(data):
    num_columns = len(data[0])
    latex_str = '\\begin{tabular}{ |' + '|'.join(['c'] * num_columns) + '| }\n'
    latex_str += '\\hline\n'

    for row in data:
        latex_str += ' & '.join(row) + ' \\\\\n'
        latex_str += '\\hline\n'

    latex_str += '\\end{tabular}'

    return latex_str

def picture_generation(path_to_image):
    latex_str = "\\begin{figure}[h]\n"
    latex_str += "\\centering\n"
    latex_str += "\\includegraphics[width=0.8\linewidth]{" + path_to_image + "}\n"
    #latex_str += "\\caption{" + caption + "}\n"
    latex_str += "\\end{figure}"

    return latex_str