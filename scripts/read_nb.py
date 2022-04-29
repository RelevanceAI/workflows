import os
from pathlib import Path
from nbformat import read, NO_CONVERT

# Each of the below aims to extract the lreevant cell metadata
def get_cell_type(cell):
    print(cell)
    if "tags" in cell:
        if len(cell["metadata"]["tags"]) > 0:
            return cell["metadata"]["tags"][0]
    return []


def extract_info_from_cell_type(cells, cell_type, fn):
    for cell in cells:
        if get_cell_type(cell) == cell_type:
            return cell[0]["source"]
    raise ValueError(f"Missing {cell_type} in {fn}")


def get_notebook_cells(nb_path):
    with open(nb_path) as fp:
        notebook = read(fp, NO_CONVERT)
    return notebook["cells"]


def extract_info_from_notebook(nb_path, cell_type):
    cells = get_notebook_cells(nb_path)
    return extract_info_from_cell_type(cells, cell_type, nb_path)


def get_description(notebook):
    cells = get_notebook_cells(notebook)
    code_cells = [c for c in cells if c["cell_type"] == "markdown"]
    for no_cell, cell in enumerate(code_cells):
        if no_cell == 2:
            return cell["source"]
    return ""


def get_prerequisites(fn):
    return extract_info_from_notebook(fn, "prerequisites")


def get_use_cases(fn):
    return extract_info_from_notebook(fn, "use_cases")


def get_documentation_link(fn):
    return extract_info_from_notebook(fn, "documentation_link")


def get_video_link(fn):
    return extract_info_from_notebook(fn, "video_link")


if __name__ == "__main__":
    # nb_full_path = "'workflows/bias-detection/✨Vector_Based_Bias_Detection_With_Relevance_AI.ipynb"
    # nb_full_path = os.path.join("workflows", nb_name)
    files = Path("workflows").rglob("*.ipynb")
    nb_full_path = list(files)[1].__str__()
    results = get_prerequisites(nb_full_path)
    print(results)
    results = get_documentation_link(nb_full_path)
    print(results)
    results = get_description(nb_full_path)
    print(results)
