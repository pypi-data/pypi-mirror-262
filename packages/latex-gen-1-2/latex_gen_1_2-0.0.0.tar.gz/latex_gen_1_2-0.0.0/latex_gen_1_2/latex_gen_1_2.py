def generate_table(data):
    if not data:
        return ''

    num_columns = len(data[0])
    table_code = '\\begin{tabular}{|' + '|'.join(['c' for _ in range(num_columns)]) + '|}\n'
    table_code += '\\hline\n'

    for row in data:
        table_code += ' & '.join(str(cell) for cell in row) + ' \\\\\n'
        table_code += '\\hline\n'

    table_code += '\\end{tabular}\n'

    return table_code

def generate_image(image_path, caption='Fig. 1'):
    latex_code = '\\begin{figure}[h!]\n'
    latex_code += '\\centering\n'
    latex_code += '\\includegraphics[width=0.5\\textwidth]{' + image_path + '}\n'
    latex_code += '\\caption{' + caption + '}\n'
    latex_code += '\\end{figure}\n'

    return latex_code