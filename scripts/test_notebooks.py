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
    "Credentials",
    ["project", "api_key", "region", "firebase_uid", "token", "base64_token"],
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


def get_credentials(path: Path, workflow_tokens: dict, region: str) -> Credentials:
    """
    Get credentials required to initialize Relevance AI client.
    """
    base64_token = workflow_tokens.get("WORKFLOW_TOKEN_" + path.stem.upper())
    if base64_token is not None:
        preconfiguration = json.loads(base64.b64decode(base64_token + "==="))
        project = preconfiguration["project"]
        api_key = preconfiguration["api_key"]
        region = preconfiguration["region"]
        token = preconfiguration["authorizationToken"]
        firebase_uid = token.split(":")[-1]

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

    return Credentials(project, api_key, region, firebase_uid, token, base64_token)


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


def cell_find_replace(cell_source: List[str], find_str_regex: str, replace_str: str):
    if isinstance(cell_source, str):
        cell_source = [cell_source]
    for i, cell_source_str in enumerate(cell_source):
        if bool(re.search(find_str_regex, cell_source_str)):
            find_replace_str = re.search(find_str_regex, cell_source_str).group()
            logging.debug(f"Found str within sentence: {find_replace_str.strip()}")
            logging.debug(f"Replace str: {replace_str}")
            cell_source_str = cell_source_str.replace(find_replace_str, replace_str)
            logging.debug(f"Updated: {cell_source_str.strip()}")
            cell_source[i] = cell_source_str
    return cell_source


def insert_credentials(notebook: dict, credentials: Credentials) -> None:
    """
    Modifies a notebook (formatted as a dictionary) so that the Relevance AI
    client has the proper credentials. In the event that the notebook is
    activated by a token, credentials will not be added.
    """
    CONFIG_BASE64_REGEX = ".*base64.b64decode.*"
    for cell in notebook["cells"]:
        if cell["cell_type"] == "code":
            ## Checking if core workflow
            if bool(re.search(CONFIG_BASE64_REGEX, str(cell["source"]))):
                if not credentials.base64_token:
                    ERROR_MESSAGE = f"""Cannot find base64 token required for < {notebook["metadata"]["colab"]["name"]} >. \
                        Please set env variable - export WORKFLOW_TOKEN_{notebook["metadata"]["colab"]["name"].replace(" ", "_").split(".ipynb")[0].upper()}=<DASHBOARD_WORKFLOW_BASE64_TOKEN>
                    """
                    raise ValueError(ERROR_MESSAGE)

                ## Replacing core workflow tokens
                TOKEN_PARAM_REGEX = 'token.*=.*#@param {type:"string"}'

                TOKEN_REPLACE_STR_REPLACE = f'token="{credentials.base64_token}"\n'
                token_args = {
                    "find_str_regex": TOKEN_PARAM_REGEX,
                    "replace_str": TOKEN_REPLACE_STR_REPLACE,
                }

                if bool(re.search(TOKEN_PARAM_REGEX, str(cell["source"]))):
                    logging.info(f"Replacing base64 token ...")
                    logging.debug(f"Found sentence: {str(cell['source'])}")
                    logging.debug(f"Find string regex: {TOKEN_PARAM_REGEX}")
                    cell["source"] = "".join(
                        cell_find_replace(cell["source"], **token_args)
                    )
                    logging.info(f'\n----\n{cell["source"]}\n---\n')
                    break

            else:
                CLIENT_INSTANTIATION_SENT_REGEX = "Client\(.*\)"
                CLIENT_INSTANTIATION_STR_REGEX = "\((.*?)\)"

                # CLIENT_INSTANTIATION_BASE = f"client = Client()"
                TEST_ACTIVATION_TOKEN = (
                    credentials.token
                    if credentials.token
                    else f"{credentials.project}:{credentials.api_key}:{credentials.region}:{credentials.firebase_uid}"
                )
                CLIENT_INSTANTIATION_STR_REPLACE = f'(token="{TEST_ACTIVATION_TOKEN}")'

                client_instantiation_args = {
                    "find_str_regex": CLIENT_INSTANTIATION_STR_REGEX,
                    "replace_str": CLIENT_INSTANTIATION_STR_REPLACE,
                }

                if bool(
                    re.search(CLIENT_INSTANTIATION_SENT_REGEX, str(cell["source"]))
                ):
                    logging.info(f"Replacing client ...")
                    logging.debug(f"Found sentence: {str(cell['source'])}")
                    logging.debug(
                        f"Find string regex: {CLIENT_INSTANTIATION_SENT_REGEX}"
                    )
                    cell["source"] = "".join(
                        cell_find_replace(cell["source"], **client_instantiation_args)
                    )
                    logging.info(f'\n----\n{cell["source"]}\n---\n')
                    break
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
        logging.info(error_header)
        mask_credentials(result, credentials)
        logging.info(result["error"])
        logging.info(error_footer)


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
        logging.info("No errors occurred while checking notebooks.")


def main(args):
    logging_level = logging.DEBUG if args.debug else logging.INFO
    # logging.basicConfig(format='%(asctime)s %(message)s', level=logging_level)
    logging.basicConfig(level=logging_level)

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
    parser.add_argument("-d", "--debug", action="store_true", help="Run debug mode")
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
