def TEXtable(data: list[list]) -> str:
    """
    This function converts the data
    into a latex table code.
    """
    
    def format_row(row: list[list]) -> str:
        return " & ".join(map(str, row)) + " \\\\\n"
    
    def format_table(rows: list[list]) -> str:
        if len(rows) == 0 or len(rows[0]) == 0 or type(rows) != list:
            return error_handling()
        
        num_cols = len(rows[0])
        
        formatted_rows = map(format_row, rows)
        table_content = "".join(formatted_rows)
        
        latex_table = "\\begin{tabular}{|" + "c|" * num_cols + "}\n"
        latex_table += "\\hline\n"
        latex_table += table_content
        latex_table += "\\hline\n"
        latex_table += "\\end{tabular}"
        return latex_table

    def error_handling() -> str:
        return "Error in the table data."
    
    return format_table(data)


def TEXimage(image_path: str) -> str:
    """
    This function converts the image path
    into a latex image code.
    """

    def format_image(image_path: str) -> str:
        if len(image_path) == 0 or image_path.find(".png") == -1 or type(image_path) != str:
            return error_handling()
        
        latex_image = f"\\begin{{figure}}[h]\n"
        latex_image += "\\centering\n"
        latex_image += f"\\includegraphics[max width=\\textwidth,max height=\\textheight]{{{image_path}}}\n"
        latex_image += f"\\end{{figure}}"
        return latex_image
    
    def error_handling() -> str:
        return "Error in the image path.\n"
    
    return format_image(image_path)


def TEXdocument(table_data="", image_path="") -> str:
    """
    This function converts the data
    into a valid latex document code.
    """
    
    latex_preamble = (
        "\\documentclass[12pt]{article}\n"
        "\\usepackage{amsmath}\n"
        "\\usepackage{graphicx}\n"
        "\\usepackage{hyperref}\n"
        "\\usepackage[latin1]{inputenc}\n"
        "\\usepackage[export]{adjustbox}\n\n"
        "\\begin{document}\n"
        "\\centering\n\n"
    )

    latex_document = latex_preamble

    if table_data != "":
        table_code = TEXtable(table_data)
        latex_document += table_code + "\n\n"
    
    if image_path != "":
        image_code = TEXimage(image_path)
        latex_document += image_code + "\n\n"
        
    latex_document += "\\end{document}"

    return latex_document
