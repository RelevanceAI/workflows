#!/usr/bin/env python3

from pathlib import Path
import sys, os, re, itertools
from typing import Iterable, List, Union
from typing_extensions import Literal
import logging
import argparse
import json

API_KEY_MIN_ENTROPY_RATIO = 0.5
API_KEY_MIN_LENGTH = 20


def cell_find_replace(
    cell_source: List[str],
    find_str_regex: str,
    replace_str: str,
    str_exclude: List[str] = None,
):
    """
    Takes a list of cell sources, finds a string within the list of cells, and replaces
    it with a new string
    """
    if isinstance(cell_source, str):
        cell_source = [cell_source]
    for i, cell_source_str in enumerate(cell_source):
        if bool(re.search(find_str_regex, cell_source_str)):
            find_replace_str = re.search(find_str_regex, cell_source_str).group()
            logging.debug(f"Found str within sentence: {find_replace_str.strip()}")
            if str_exclude and any(s in find_replace_str for s in str_exclude):
                logging.info(f"Excluding {str_exclude}")
                continue
            logging.debug(f"Replace str: {replace_str}")
            cell_source_str = cell_source_str.replace(find_replace_str, replace_str)
            logging.debug(f"Updated: {cell_source_str.strip()}")
            cell_source[i] = cell_source_str
    return cell_source


def pairwise(iterable: Iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def token_is_api_key(token: str):
    """
    Returns True if the token is an API key or password.
    """
    if len(token) < API_KEY_MIN_LENGTH:
        return (False, "")
    entropy = 0
    for a, b in pairwise(list(token)):
        if not (
            (str.islower(a) and str.islower(b))
            or (str.isupper(a) and str.isupper(b))
            or (str.isdigit(a) and str.isdigit(b))
        ):
            entropy += 1
    return (
        float(entropy) / len(token) > API_KEY_MIN_ENTROPY_RATIO,
        float(entropy) / len(token),
    )


def line_contains_api_key(line: str, regex_str: str):
    """
    Returns True if any token in the line contains an API key or password.
    """
    for token_match in re.finditer(regex_str, line):
        token = (
            token_match.group()
            .split("=")[-1]
            .split("#@param")[0]
            .replace('"', "")
            .replace("'", "")
            .strip()
        )
        if token and not any([f in token for f in ["token", "config"]]):
            result = token_is_api_key(token)
            if result:
                return (True, result[1])
    return (False, "")


def clean_keys(cell_source: List[str]):
    api_re_match = [
        {
            "sent_regex": "client\s*=\s*Client(.*)",
            "str_regex": "(token\s*=\s*['\"A-Za-z0-9-:]+)",
            "str_exclude": ["config['authorizationToken']", "#@param"],
            "replace": "",
        },
        {
            "sent_regex": "token\s*=\s*.*#@param.*",
            "str_regex": "token\s*=\s*.*#@param.*",
            "replace": 'token = "" #@param {type:"string"}',
        },
    ]

    for re_replace in api_re_match:
        if bool(re.search(re_replace["sent_regex"], str(cell_source))):
            cell_source = cell_find_replace(
                cell_source,
                re_replace["str_regex"],
                re_replace["replace"],
                re_replace.get("str_regex_exclude"),
            )
    return cell_source


def scan_file(fpath: Path, show_keys=False, clean=True):
    """
    Prints out lines in the specified file that probably contain an API key or password.
    """
    logging.info(f"Scanning {fpath}...")

    for api_prefix in ["project", "api_key", "token"]:
        API_REGEX_STR = f"{api_prefix}\s*=\s*['\"A-Za-z0-9-:]+"
        if fpath.endswith(".ipynb"):
            f = json.loads(open(fpath).read())
            for i, cell in enumerate(f["cells"]):
                if bool(re.search(API_REGEX_STR, str(cell["source"]))):
                    if isinstance(cell["source"], str):
                        cell["source"] = [cell["source"]]
                    for i, cell_source in enumerate(cell["source"]):
                        result = line_contains_api_key(
                            cell_source.strip(), API_REGEX_STR
                        )
                        if result[0]:
                            logging.info(
                                f"\033[1m{fpath}: Line {i}: Entropy {result[1]}\033[0m {API_REGEX_STR}"
                            )

                            if show_keys:
                                logging.info(f"\n\033[1m{cell_source}\033[0m")

                            if clean:

                                cell["source"] = "".join(clean_keys(cell_source))
                                json.dump(f, fp=open(fpath, "w"), indent=4)
                            raise ValueError(
                                f"API key found in file {fpath}: Line {i+1}"
                            )

        elif fpath.endswith(".md"):
            f = open(fpath)
            for i, line in enumerate(f):
                result = line_contains_api_key(line, API_REGEX_STR)
                if result[0]:
                    logging.info(
                        f"\033[1m{fpath}: Line {i} : Entropy {result[1]}\033[0m {API_REGEX_STR}"
                    )
                    if show_keys:
                        logging.info(f"\n\033[1m{line}\033[0m")
                    raise ValueError(f"API key found in file {fpath}: Line {i+1}")


def get_files(
    path: Union[Path, str], ext: Literal["md", "ipynb"], exclude: List[str] = None
):
    files = Path(path).glob(f"**/*.{ext}")
    return [
        f
        for f in files
        if exclude
        if not any(exclude_str in str(f) for exclude_str in exclude)
    ]


def main(args):
    logging_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=logging_level)
    # logging.basicConfig(format='%(asctime)s %(message)s', level=logging_level)

    logging.info(f"Scanning directory: {args.path}")
    logging.info(f"For tokens with minimum API key length: {API_KEY_MIN_LENGTH}")
    logging.info(f"For tokens with minimum entropy ratio: {API_KEY_MIN_ENTROPY_RATIO}")

    md_files = get_files(args.path, ext="md")
    notebooks = get_files(
        args.path, ext="ipynb", exclude=[".ipynb_checkpoints", "_prod.ipynb"]
    )

    for f in itertools.chain(md_files, notebooks):
        scan_file(str(f), show_keys=args.show_keys, clean=args.clean)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    ROOT_PATH = Path(__file__).parent.resolve() / ".."

    parser.add_argument("-d", "--debug", help="Run debug mode", action="store_true")
    parser.add_argument("-p", "--path", default=ROOT_PATH, help="Path of root folder")
    parser.add_argument(
        "-ml",
        "--min-length",
        default=API_KEY_MIN_LENGTH,
        help="Minimum length of API key",
    )
    parser.add_argument(
        "-er",
        "--entropy-ratio",
        default=API_KEY_MIN_ENTROPY_RATIO,
        help="Minimum entropy ratio of API key",
    )
    parser.add_argument(
        "-s", "--show-keys", action="store_true", help="Whether to show API key"
    )
    parser.add_argument(
        "-c",
        "--clean",
        action="store_true",
        help="Whether to clean API keys in notebook",
    )

    args = parser.parse_args()

    main(args)
