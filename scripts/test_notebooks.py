import logging
import os
import re

from pathlib import Path
from typing import List

import nbformat
from nbclient import NotebookClient

# Any notebooks that should be ignored should be listed in IGNORED. They can
# be either a string or wrapped in Path().
IGNORED = frozenset([])

WORKFLOWS = Path(__file__).parent.parent / Path("workflows")

logging.basicConfig(level=logging.INFO)

def get_paths() -> List[Path]:
    """
    Get paths of all of the Jupyter Notebooks that will be tested.
    """
    with open(WORKFLOWS / Path("ignore-workflows.txt")) as file:
        ignored_notebooks = set(
            WORKFLOWS / Path(notebook.strip())
            for notebook in file.readlines()
            if not notebook.startswith('#')
        )
    logging.info(
        "Ignoring the following notebooks: " +
        ", ".join(map(
            lambda notebook: str(notebook),
            ignored_notebooks
        ))
    )

    workflows = [
        workflow_dir for workflow_dir in WORKFLOWS.iterdir()
        if workflow_dir.is_dir()
    ]
    paths = []
    for workflow in workflows:
        paths.extend([
            notebook for notebook in workflow.iterdir()
            if (
                notebook.suffix == ".ipynb" and
                notebook not in ignored_notebooks
            )
        ])
    logging.info(
        "Checking the following notebooks: " +
        ", ".join(map(
            lambda path: str(path),
            paths 
        ))
    )
    
    return paths

def insert_credentials(notebook: dict, region: str) -> None:
    """
    Modifies a notebook (formatted as a dictionary) so that the Relevance AI
    client has the proper credentials.
    """
    if region == "us-east-1":
        project = os.getenv("TEST_US_PROJECT")
        api = os.getenv("TEST_US_API_KEY")
    elif region == "old-australia-east":
        project = os.getenv("TEST_PROJECT")
        api = os.getenv("TEST_API_KEY")
    else:
        raise ValueError("Invalid region")

    for cell in notebook["cells"]:
        if cell["cell_type"] == "code":
            source = cell["source"]
            regex_result = re.search("Client\(.*\)", source)
            if regex_result is not None:
                start, end = regex_result.span()
                # comma at the end is in case Client has existing arguments
                credentials = f"project=\"{project}\",api_key=\"{api}\","
                cell["source"] = "".join([
                    source[:start+6+1], # 'Client' has length 6
                    credentials,
                    source[start+6+1:] 
                ])
                break # No need to continue after inserting credentials
        else:
            continue
    
    return notebook

def generate_notebooks(paths: List[Path], region: str) -> List[dict]:
    """
    Map each path into a notebook (formatted as a dictionary) and ensure that
    the Relevance AI client, if the notebook calls it, has the proper
    credentials.
    """
    return [
        insert_credentials(
            nbformat.read(path, nbformat.NO_CONVERT),
            region
        ) for path in paths
    ]

def get_notebooks(region: str) -> List[dict]:
    """
    Gets and sets all notebooks to be checked.
    """
    return generate_notebooks(get_paths(), region)

def execute_notebook(notebook: dict):
    """
    Executes a single notebook.
    """
    client = NotebookClient(
        notebook,
        timeout=600,
        kernel_name="relevanceai"
    )
    client.execute()

def execute_notebooks(notebooks: List[dict]):
    """
    Executes multiple notebooks in paralle. 
    """
    pass

if __name__ == "__main__":
    notebooks = get_notebooks(region="us-east-1")
    notebook = notebooks[0]
    execute_notebook(notebook)

    #nb_path = get_notebooks()[5]
    #nb_path = get_notebooks()[7] # SUCCESS
    #print(execute_notebook(nb_path))