import logging
import os
import re

from collections import namedtuple
from multiprocessing import Pool
from pathlib import Path
from typing import List, Optional

import nbformat

from nbclient import NotebookClient

WORKFLOWS = Path(__file__).resolve().parent.parent / Path("workflows")

logging.basicConfig(level=logging.INFO)

Credentials = namedtuple("Credentials", ["project", "api_key", "region"])

def get_credentials(region: str) -> Credentials:
    """
    Get credentials required to initialize Relevance AI client.
    """
    if region == "us-east-1":
        project = os.getenv("TEST_US_PROJECT")
        api_key = os.getenv("TEST_US_API_KEY")
    elif region == "old-australia-east":
        project = os.getenv("TEST_PROJECT")
        api_key = os.getenv("TEST_API_KEY")
    else:
        raise ValueError("Invalid region")
    
    return Credentials(project, api_key, region)

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
        "".join(map(
            lambda notebook: f"\n  * {str(notebook)}",
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
        "".join(map(
            lambda path: f"\n  * {str(path)}",
            paths 
        ))
    )
    
    return paths

def insert_credentials(
    notebook: dict, credentials: Credentials
) -> None:
    """
    Modifies a notebook (formatted as a dictionary) so that the Relevance AI
    client has the proper credentials.
    """
    for cell in notebook["cells"]:
        if cell["cell_type"] == "code":
            source = cell["source"]
            regex_result = re.search("Client\(.*\)", source)
            if regex_result is not None:
                start, end = regex_result.span()
                # comma at the end is in case Client has existing arguments
                cell["source"] = "".join([
                    source[:start+6+1], # 'Client' has length 6
                    "project=\"{}\",api_key=\"{}\",region=\"{}\",".format(
                        credentials.project,
                        credentials.api_key,
                        credentials.region
                    ),
                    source[start+6+1:] 
                ])
                break # No need to continue after inserting credentials
        else:
            continue
    
    return notebook

def insert_name(notebook: dict, path: Path) -> dict:
    """
    Insert a name into the notebook metadata for bookkeeping.
    """
    name = str(path.stem)
    notebook["metadata"]["temporary_name"] = name
    return notebook

def generate_notebooks(
    paths: List[Path],
    credentials: Credentials
) -> List[dict]:
    """
    Map each path into a notebook (formatted as a dictionary) and ensure that
    the Relevance AI client, if the notebook calls it, has the proper
    credentials.
    """
    return [
        insert_name(
            insert_credentials(
                nbformat.read(path, nbformat.NO_CONVERT),
                credentials
            ),
            path
        ) for path in paths
    ]

def get_notebooks(credentials: Credentials) -> List[dict]:
    """
    Gets and sets all notebooks to be checked.
    """
    return generate_notebooks(
        get_paths(),
        credentials
    )

def execute_notebook(notebook: dict) -> dict:
    """
    Executes a single notebook.
    """
    notebook_name = notebook["metadata"]["temporary_name"]
    logging.info(f"Checking {notebook_name}")
    try:
        client = NotebookClient(
            notebook,
            timeout=600,
            kernel_name="python3"
        )
        client.execute()
        return {}
    except Exception as err:
        return {"notebook": notebook_name, "error": err}

def execute_notebooks(
    notebooks: List[dict],
    processes: Optional[int] = None,
    chunksize: Optional[int] = 1,
):
    """
    Executes multiple notebooks in parallel. 
    """
    with Pool(processes=processes) as pool:
        return pool.map(execute_notebook, notebooks, chunksize=chunksize)

def mask_credentials(result: dict, credentials: Credentials) -> None:
    """
    Masks the credentials, if they exist, in the error content in place.
    """
    error: str = result["error"].traceback

    # Preemptively ensure that the project and API key are masked in the
    # error message, if it shows up at all.
    error = error.replace(
        credentials.project,
        "*" * len(credentials.project)
    )
    error = error.replace(
        credentials.api_key,
        "*" * len(credentials.api_key)
    )

    result["error"].traceback = error

def print_error(result: dict, credentials: Credentials) -> None:
    """
    Print the error message, if the result contains errors.
    """
    if result:
        error_header = "{:=^128}".format(f"ERROR IN {result['notebook']}")
        error_footer = f"{'=' * len(error_header)}"
        print(error_header)
        mask_credentials(result, credentials)
        print(result["error"])
        print(error_footer)

def print_errors(results: List[dict], credentials: Credentials) -> None:
    """
    Print the errors of multiple results, if the results contain errors, and
    raise an error at the end (again, if there exists any errors).
    """
    if any(results):
        # If there are any non-empty results, that means an error occurred
        for result in results:
            print_error(result, credentials)
        else:
            raise Exception("At least one of the notebook checks failed.")
    else:
        print("No errors occurred while checking notebooks.")

if __name__ == "__main__":
    region = "us-east-1"
    credentials = get_credentials(region)
    notebooks = get_notebooks(credentials)
    results = execute_notebooks(notebooks)
    print_errors(results, credentials)
