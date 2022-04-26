import base64
import json
import logging
import os
import re
import argparse

from collections import namedtuple
from multiprocessing import Pool
from pathlib import Path
from typing import List, Optional

import nbformat

from nbclient import NotebookClient


WORKFLOWS = Path(__file__).resolve().parent.parent / Path("workflows")

logging.basicConfig(level=logging.INFO)

Credentials = namedtuple(
    "Credentials", ["project", "api_key", "region", "firebase_uid", "token"]
)


def get_paths() -> List[Path]:
    """
    Get paths of all of the Jupyter Notebooks that will be tested.
    """
    with open(WORKFLOWS / Path("ignore-workflows.txt")) as file:
        ignored_notebooks = set(
            WORKFLOWS / Path(notebook.replace("#", "").strip())
            for notebook in file.readlines()
            if notebook.startswith("#")
            and any(nb_path_string in notebook for nb_path_string in ["/", "ipynb"])
            and "workflow" not in notebook
        )
    logging.info(
        "Ignoring the following notebooks: "
        + "".join(map(lambda notebook: f"\n  * {str(notebook)}", ignored_notebooks))
    )

    workflows = [
        workflow_dir for workflow_dir in WORKFLOWS.iterdir() if workflow_dir.is_dir()
    ]
    paths = []
    for workflow in workflows:
        paths.extend(
            [
                notebook
                for notebook in workflow.iterdir()
                if (notebook.suffix == ".ipynb" and notebook not in ignored_notebooks)
            ]
        )
    logging.info(
        "Checking the following notebooks: "
        + "".join(map(lambda path: f"\n  * {str(path)}", paths))
    )

    return paths


def get_credentials(path: Path, tokens: dict, region: str) -> Credentials:
    """
    Get credentials required to initialize Relevance AI client.
    """
    base64_token = tokens.get("WORKFLOW_TOKEN_" + path.stem.upper())
    if base64_token is not None:
        preconfiguration = json.loads(base64.b64decode(base64_token + "==="))
        project = preconfiguration["project"]
        api_key = preconfiguration["api_key"]
        region = preconfiguration["region"]
        firebase_uid = preconfiguration["firebase_uid"]
        token = f"{project}:{api_key}:{region}:{firebase_uid}"
    else:
        if region == "us-east-1":
            project = os.getenv("TEST_US_PROJECT")
            api_key = os.getenv("TEST_US_API_KEY")
            firebase_uid = os.getenv("TEST_FIREBASE_UID")
            token = os.getenv("TEST_ACTIVATION_TOKEN")
        elif region == "ap-southeast-2":
            project = os.getenv("TEST_PROJECT")
            api_key = os.getenv("TEST_API_KEY")
            firebase_uid = os.getenv("TEST_FIREBASE_UID")
            token = os.getenv("TEST_ACTIVATION_TOKEN")
        elif region == "old-australia-east":
            project = os.getenv("TEST_PROJECT")
            api_key = os.getenv("TEST_API_KEY")
        else:
            raise ValueError("Invalid region")

    return Credentials(project, api_key, region, firebase_uid, token)


def get_all_credentials(paths: List[Path], region: str) -> List[Credentials]:
    """
    Retrieves the credentials for each notebook execution. Each notebook
    merits its own credentials because it may be different if it uses a
    token.
    """
    workflow_tokens = {
        token: os.environ[token]
        for token in filter(lambda var: var.startswith("WORKFLOW_TOKEN"), os.environ)
    }
    return [get_credentials(path, workflow_tokens, region) for path in paths]


def notebook_find_replace(
    fname: str, find_sent_regex: str, find_str_regex: str, replace_str: str
):
    logging.info(f"\tInput: {fname}")
    notebook_json = json.loads(open(fname).read())

    for cell in notebook_json["cells"]:
        if bool(re.search(find_sent_regex, str(cell["source"]))):
            logging.debug(f"Found sentence: {str(cell['source'])}")
            logging.debug(f"Find string regex: {find_str_regex}")
            for i, cell_source in enumerate(cell["source"]):
                if bool(re.search(find_str_regex, cell_source)):
                    find_replace_str = re.search(find_str_regex, cell_source).group()
                    logging.debug(
                        f"Found str within sentence: {find_replace_str.strip()}"
                    )
                    logging.debug(f"Replace str: {replace_str}")
                    cell_source = cell_source.replace(find_replace_str, replace_str)
                    logging.debug(f"Updated: {cell_source.strip()}")
                    cell["source"][i] = cell_source

    logging.info(f"\tOutput file: {fname}")
    json.dump(notebook_json, fp=open(fname, "w"), indent=4)


def insert_credentials(notebook: dict, credentials: Credentials) -> None:
    """
    Modifies a notebook (formatted as a dictionary) so that the Relevance AI
    client has the proper credentials. In the event that the notebook is
    activated by a token, credentials will not be added.
    """
    for cell in notebook["cells"]:
        # Simultaneously check for both the token and client works correctly
        # because the token must be defined before client in the notebook. A
        # sufficient condition to execute the notebook when exactly one of
        # these are filled.
        if cell["cell_type"] == "code":
            source = cell["source"]

            # token_regex = re.search(
            #     "(token\s*=\s*(\"|\'))(.*?(\"|\'))",
            #     #"token\s*=\s*((\".*?\")|(\'.*?\'))",
            #     source
            # )
            # if token_regex is not None:
            #     start, end = token_regex.span()
            #     print(cell["source"])
            #     cell["source"] = "".join([
            #         source[:start],
            #         token_regex.group(1),
            #         credentials.token,
            #         token_regex.group(2)[-1], # add back the '"'
            #         source[end:]
            #     ])
            #     break # If a token exists, no need to go further

            client_regex = re.search("Client\(.*\)", source)

            if client_regex is not None:
                start, end = client_regex.span()
                # comma at the end is in case Client has existing arguments

                cell["source"] = "".join(
                    [
                        source[: start + 6 + 1],  # 'Client(' has length 6 + 1
                        f"token='{credentials.project}:{credentials.api_key}:{credentials.region}:{credentials.firebase_uid}'",
                        source[start + 6 + 1 :],
                    ]
                )

                break  # No need to continue after inserting credentials
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
    paths: List[Path], all_credentials: List[Credentials]
) -> List[dict]:
    """
    Map each path into a notebook (formatted as a dictionary) and ensure that
    the Relevance AI client, if the notebook calls it, has the proper
    credentials.
    """
    return [
        insert_name(
            insert_credentials(nbformat.read(path, nbformat.NO_CONVERT), credentials),
            path,
        )
        for path, credentials in zip(paths, all_credentials)
    ]


def get_notebooks(paths: List[Path], all_credentials: List[Credentials]) -> List[dict]:
    """
    Gets and sets all notebooks to be checked.
    """
    return generate_notebooks(paths, all_credentials)


def execute_notebook(notebook: dict) -> dict:
    """
    Executes a single notebook.
    """
    notebook_name = notebook["metadata"]["temporary_name"]
    logging.info(f"Checking {notebook_name}")
    try:
        client = NotebookClient(notebook, timeout=600, kernel_name="python3")
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
    error = (
        error.replace(credentials.project, "*" * len(credentials.project))
        if credentials.project
        else error
    )
    error = (
        error.replace(credentials.api_key, "*" * len(credentials.api_key))
        if credentials.api_key
        else error
    )
    error = (
        error.replace(credentials.firebase_uid, "*" * len(credentials.firebase_uid))
        if credentials.firebase_uid
        else error
    )
    error = (
        error.replace(credentials.token, "*" * len(credentials.token))
        if credentials.token
        else error
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


def print_errors(results: List[dict], all_credentials: List[Credentials]) -> None:
    """
    Print the errors of multiple results, if the results contain errors, and
    raise an error at the end (again, if there exists any errors).
    """
    if any(results):
        # If there are any non-empty results, that means an error occurred
        for result, credentials in zip(results, all_credentials):
            print_error(result, credentials)
        else:
            raise Exception("At least one of the notebook checks failed.")
    else:
        print("No errors occurred while checking notebooks.")


def main(args):

    if args.notebooks:
        paths = [Path(WORKFLOWS / path) for path in args.notebooks]
    else:
        paths = get_paths()
    all_credentials = get_all_credentials(paths, args.region)
    notebooks = get_notebooks(paths, all_credentials)
    results = execute_notebooks(notebooks)
    print_errors(results, all_credentials)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-r", "--region", default="ap-southeast-2", help="Default region"
    )
    parser.add_argument(
        "-n",
        "--notebooks",
        nargs="+",
        default=None,
        help="List of notebooks to execute",
    )
    args = parser.parse_args()
    main(args)
