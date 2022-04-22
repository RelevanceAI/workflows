#!/usr/bin/env python3

from pathlib import Path
import sys, os, re, itertools
from typing import Iterable, Literal, Union
import logging
import argparse
import json

API_KEY_MIN_ENTROPY_RATIO = 0.5
API_KEY_MIN_LENGTH = 20

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
		return (False, '')
	entropy = 0
	for a, b in pairwise(list(token)):
		if not ((str.islower(a) and str.islower(b)) or (str.isupper(a) and\
			str.isupper(b)) or (str.isdigit(a) and str.isdigit(b))):
			entropy += 1
	return (float(entropy) / len(token) > API_KEY_MIN_ENTROPY_RATIO, float(entropy) / len(token))

def line_contains_api_key(line: str, regex_str: str):
	"""
	Returns True if any token in the line contains an API key or password.
	"""
	for token_match in re.finditer(regex_str, line):
		token = token_match.group().split('=')[-1]
		if token!='token' and token!='config':
			result = token_is_api_key(token)
			if result:
				return (True, result[1])
	return (False, '')

def scan_file(fpath: Path, show_keys=False):
	"""
	Prints out lines in the specified file that probably contain an API key or password.
	"""
	logging.info(f'Scanning {fpath}...')

	PROJECT_REGEX_STR='(project=[\'\"A-Za-z0-9-:]+)'
	API_KEY_REGEX_STR='(api_key=[\'\"A-Za-z0-9-:]+)'
	TOKEN_REGEX_STR='(token=[\'\"A-Za-z0-9-:]+)'

	for API_REGEX_STR in [PROJECT_REGEX_STR, API_KEY_REGEX_STR, TOKEN_REGEX_STR]:
		if fpath.endswith('.ipynb'):
			f = json.loads(open(fpath).read())
			for i, cell in enumerate(f['cells']):
				if bool(re.search(TOKEN_REGEX_STR, str(cell["source"]))):
					for i, cell_source in enumerate(cell["source"]):
						result = line_contains_api_key(cell_source.strip(), API_REGEX_STR)
						if result[0]:
							logging.info(f'\033[1m{fpath}: Line {i}: Entropy {result[1]}\033[0m {API_REGEX_STR}')
							if show_keys:
								logging.info(f'\n\033[1m{cell_source}\033[0m')
							raise ValueError(f'API key found in file {fpath}: Line {i+1}')
		elif fpath.endswith('.md'):
			f = open(fpath)
			for i,  line in enumerate(f):
				result = line_contains_api_key(line, API_REGEX_STR)
				if result[0]:
					logging.info(f'\033[1m{fpath}: Line {i} : Entropy {result[1]}\033[0m {API_REGEX_STR}')
					if show_keys:
						logging.info(f'\n\033[1m{line}\033[0m')
					raise ValueError(f'API key found in file {fpath}: Line {i+1}')


def get_files(path: Union[Path, str], ext: Literal['md', 'ipynb']):
	return Path(path).glob(f"**/*.{ext}")


def main(args):
	logging_level = logging.DEBUG if args.debug else logging.INFO
	logging.basicConfig(level=logging_level)
	# logging.basicConfig(format='%(asctime)s %(message)s', level=logging_level)

	logging.info(f'Scanning directory: {args.path}')
	logging.info(f'For tokens with minimum API key length: {API_KEY_MIN_LENGTH}')
	logging.info(f'For tokens with minimum entropy ratio: {API_KEY_MIN_ENTROPY_RATIO}')

	md_files = get_files(args.path, ext='md')
	notebooks = get_files(args.path, ext='ipynb')

	for f in itertools.chain(md_files, notebooks):
		print(args.show_keys)
		scan_file(str(f), show_keys=args.show_keys)


if __name__ == "__main__":
	parser = argparse.ArgumentParser()

	ROOT_PATH = Path(__file__).parent.resolve() / '..'

	parser.add_argument("-d", "--debug", help="Run debug mode", action='store_true')
	parser.add_argument("-p", "--path", default=ROOT_PATH, help="Path of root folder")
	parser.add_argument("-ml", "--min-length", default=API_KEY_MIN_LENGTH, help="Minimum length of API key")
	parser.add_argument("-er", "--entropy-ratio", default=API_KEY_MIN_ENTROPY_RATIO, help="Minimum entropy ratio of API key")
	parser.add_argument("-s", "--show-keys", action='store_true', help="Whether to show API key")

	args = parser.parse_args()

	main(args)
