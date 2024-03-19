from typing import Any, List
from pathlib import Path

__all__ = ["generate_tex_table", "generate_tex_document_table_image"]


def get_list_rows(data: List[Any]) -> int:
    return len(data)


def get_list_columns(data: List[List[Any]]) -> int:
    return len(data[0])


def get_tex_table_header(cols: int) -> str:
    result = ["\\begin{center}\n\\begin{tabular}{ "]
    result.append("".join(["| c "] * cols))
    result.append("| }\n\hline\n")
    return "".join(result)


def row_to_tex(data: List[str]) -> str:
    appendix = " \\\\\n"
    str_data = [str(item) for item in data]
    result = " & ".join(str_data) + appendix
    return result
    

def generate_tex_table_rows(data: List[List[str]], rows: int) -> str:
    result = []
    for row_index in range(rows):
        result.append(" " + row_to_tex(data[row_index]))
        result.append("\hline\n")
    return "".join(result)
    
    
def get_tex_table_footer() -> str:
    return "\end{tabular}\n\end{center}\n"


def generate_tex_table(input_table: List[List[str]]) -> str:
    rows = get_list_rows(input_table)
    cols = get_list_columns(input_table)
    result = get_tex_table_header(cols)
    result += generate_tex_table_rows(input_table, rows)
    result += get_tex_table_footer()
    return result


def generate_tex_image(path: str) -> str:
    result = "\includegraphics[textwidth]{"
    path = Path(path)
    result += Path(path.parent, path.stem).as_posix()
    result += "}\n"
    return result


def generate_tex_header() -> str:
    result = "\\documentclass{article}\n"
    result += "\\usepackage{graphicx}\n"
    result += "\\begin{document}\n"
    return result
    

def generate_tex_footer() -> str:
    return "\\end{document}\n"    


def gen_tex_doc_table_img(input_table: List[List[str]],
                          image_path: str) -> str:
    """
    Generates a simple document consisting of table and image
    """
    assert input_table, "Input table is not defined"
    assert image_path, "Image file path is not defined"
    assert Path(image_path).is_file(), f"Could not find image {image_path}"
    
    result = generate_tex_header()
    result += generate_tex_table(input_table)
    result += generate_tex_image(image_path)
    result += generate_tex_footer()
    return result
