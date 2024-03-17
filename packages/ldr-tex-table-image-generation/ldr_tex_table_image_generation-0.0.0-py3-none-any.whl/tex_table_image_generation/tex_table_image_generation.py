def get_tex_table(table_data):
    if not isinstance(table_data, list):
        raise ValueError("Wrong Input!")
        
    max_row_len  = 0
        
    for row in table_data:
        if not isinstance(row, list):
            raise ValueError("Wrong Input!")
        
        # на случай разной длины строк
        if len(row) > max_row_len:
            max_row_len = len(row)
    
    tex_table = "\\begin{table}[h]\n\\centering\n\\begin{tabular}{" + "|c" * max_row_len + "|}\n\\hline\n"
    
    for row in table_data:
        tex_table += " & ".join(str(element) for element in row)
        tex_table += " \\\\\n"
    
    tex_table += "\\hline\n\\end{tabular}\\end{table}\n"
    
    return tex_table

def get_tex_image(image_path, width = 0.5):
    try:
        with open(image_path, 'r') as file:
            # без использования любых библиотек по условию - так
            # но вообще os для этого используется
            pass
        
        tex_image = f'''\\begin{{figure}}[h]
\\centering
\\includegraphics[width={width}\\textwidth]{{{image_path}}}
\\end{{figure}}'''
        
        return tex_image
    except FileNotFoundError:
        raise FileNotFoundError("Wrong Input!")