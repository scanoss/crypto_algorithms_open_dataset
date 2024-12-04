# SPDX-FileCopyrightText: 2024 2024 SCAN Open Source Software SL (scanoss.com)
# SPDX-FileContributor: [Author Name(s)] <[Optional: Email Address(es)]>
#
# SPDX-License-Identifier: MIT

"""
 SPDX-License-Identifier: MIT
   Copyright (c) 2024, SCANOSS
"""
import os
import yaml
import json
import sys
import argparse
import binaryornot.check
from collections import defaultdict
from progress.spinner import Spinner
from progress.bar import Bar

__version__ = '0.0.1'
debug = False
quiet = False
trace = False
all_hidden = False  # Process hidden files/folders also


def print_stderr(*args, **kwargs):
    """
    Print the given message to STDERR
    """
    print(*args, file=sys.stderr, **kwargs)


def print_msg(*args, **kwargs):
    """
    Print message if quite mode is not enabled
    """
    if not quiet:
        print_stderr(*args, **kwargs)


def print_debug(*args, **kwargs):
    """
    Print debug message if enabled
    """
    if debug:
        print_stderr(*args, **kwargs)


def print_trace(*args, **kwargs):
    """
    Print trace message if enabled
    """
    if trace:
        print_stderr(*args, **kwargs)


def is_binary(path: str):
    """
    Check if the specified file is a potential "binary" file

    :param path: Path to the file to check
    :return: True if binary, False otherwise
    """
    if path:
        binary_path = binaryornot.check.is_binary(path)
        if binary_path:
            print_trace(f'Detected binary file: {path}')
        return binary_path
    return False


def filter_dirs(dirs: list) -> list:
    """
    Filter which folders should be considered for processing
    :param dirs: list of directories to filter
    :return: list of filtered directories
    """
    dir_list = []
    for d in dirs:
        ignore = False
        if d.startswith(".") and not all_hidden:  # Ignore all . folders unless requested
            ignore = True
        if not ignore:
            dir_list.append(d)
    return dir_list


def filter_files(files: list) -> list:
    """
    Filter which files should be considered for processing
    :param files: list of files to filter
    :return list of filtered files
    """
    file_list = []
    for f in files:
        ignore = False
        if f.startswith(".") and not all_hidden:  # Ignore all . files unless requested
            ignore = True
        if not ignore:
            file_list.append(f)
    return file_list


def load_definitions(definitions_dir: str) -> dict:
    """
    Load all the YAML definition files from the specified root folder

    :param definitions_dir: root definition folder
    :return: definition dictionary
    """
    if not definitions_dir or not os.path.exists(definitions_dir):
        print_stderr(f'Error: No definition folder specified, or it does not exist: {definitions_dir}')
        return None
    definitions = defaultdict(list)
    for root, dirs, files in os.walk(definitions_dir):
        for file in files:
            if file.endswith('.yaml') or file.endswith('.yml'):
                print_trace(f'Loading definition: {file}')
                with open(os.path.join(root, file), 'r') as yaml_file:
                    data = yaml.safe_load(yaml_file)
                    if 'keywords' in data:
                        for keyword in data['keywords']:
                            definitions[str(keyword)].append(file)
    return definitions


def analyse_file(file_path: str, definitions: dict) -> dict:
    """
    Analyse the given file for the specified definitions

    :param file_path: File to analyse
    :param definitions: definitions to search for
    :return: Dictionary of matching keywords
    """
    if not definitions:
        print_stderr(f'Error: No definitions specified.')
        return None
    if not os.path.exists(file_path):
        print_stderr(f'Error: File does not exist: {file_path}')
        return None
    if is_binary(file_path):
        return {}  # Skip binary files
    detections = []
    with open(file_path, 'rb') as file:
        print_debug(f'Analysing {file_path}...')
        contents = file.read()
        content_str = contents.decode('utf-8', 'ignore')
        if len(content_str) > 0:
            for keyword, yaml_files in definitions.items():
                keyword_str = str(keyword)
                if keyword_str in content_str:
                    match_files = []
                    for yaml_file in yaml_files:
                        match_files.append({'def_file': yaml_file})
                    detections.append({'keyword': keyword_str, 'def_files': match_files})
    return detections


def analyse_directory(target_dir: str, definitions: dict) -> list:
    """
    Analyse the given folder for the specified definitions

    :param target_dir: Target folder to scan
    :param definitions: Definitions to search for
    :return: Detection dictionary
    """
    if not target_dir or not os.path.exists(target_dir):
        print_stderr(f'Error: No target folder specified, or it does not exist: {target_dir}')
        return None
    if not definitions:
        print_stderr(f'No definitions specified to search for.')
        return None
    progress_enabled = True if not quiet and not debug and not trace and sys.stderr.isatty() else False
    spinner = None
    if progress_enabled:
        spinner = Spinner('Detecting files ')
    file_list = []
    # Walk the directory tree looking for file to analyse
    for root, dirs, files in os.walk(target_dir):
        dirs[:] = filter_dirs(dirs)  # Strip out unwanted directories
        filtered_files = filter_files(files)  # Strip out unwanted files
        for file in filtered_files:
            file_path = os.path.join(root, file)
            f_size = 0
            try:
                f_size = os.stat(file_path).st_size
            except Exception as e:
                print_trace(
                    f'Ignoring missing symlink file: {file_path} ({e})')  # Can fail if there is a broken symlink
            if f_size > 0:  # skip empty files
                if spinner:
                    spinner.next()
                file_list.append(file_path)
    if spinner:
        spinner.finish()
    all_detections = []
    # Analyse the given list of files
    if file_list:
        bar = None
        if progress_enabled:
            bar = Bar('Analysing', max=len(file_list))
            bar.next(0)
        for file_path in file_list:
            if bar:
                bar.next(1)
            detections = analyse_file(file_path, definitions)
            if detections:
                all_detections.append({'file': file_path, 'crypto': detections})
        if bar:
            bar.finish()
    return all_detections


def run_scan(target_dir: str, def_dir: str, output: str) -> bool:
    """
    Run a scan of the specified target directory using the specified keyword definitions

    :param target_dir: Target directory to scan
    :param def_dir: Definition folder to load from
    :param output: Output file to write results to
    :return: True on success, False otherwise
    """
    if not target_dir:
        print_stderr(f'Error: No target folder/directory specified.')
        return False
    if not os.path.exists(target_dir):
        print_stderr(f'Error: Target folder does not exist: {target_dir}.')
        return False
    if not def_dir:
        print_stderr(f'Error: No definition folder/directory specified.')
        return False
    if not os.path.exists(def_dir):
        print_stderr(f'Error: Definitions folder does not exist: {def_dir}.')
        return False
    if output:
        open(output, 'w').close()
    # Load the crypt definitions into memory for processing
    definitions = load_definitions(def_dir)
    if not definitions:
        print_stderr(f'Error: Failed to load definitions for: {def_dir}')
        return False
    detections = analyse_directory(target_dir, definitions)
    if detections:
        print_msg(f'Writing output to: {output}')
        results = {'files': detections}
        with open(output, 'w') as json_file:
            json.dump(results, json_file, indent=2)
    else:
        print_msg(f'No cryptography found in {target_dir}')
    return True


def setup_args():
    """
    Setup command line arguments
    :return: arguments object
    """
    global debug, quiet, trace, all_hidden
    parser = argparse.ArgumentParser(description=f'SCANOSS Keyword Analyser. Ver: {__version__}, License: MIT')
    parser.add_argument('--version', '-v', action='store_true', help='Display version details')
    parser.add_argument('target_dir', metavar='TARGET-DIR', type=str, nargs='?', help='Folder to scan')
    parser.add_argument('--definitions', '-c', type=str, default='definitions_crypto_algorithms',
                        help='The directory containing cryptography definitions (default: definitions_crypto_algorithms/)')
    parser.add_argument('--output', '-o', type=str, default='crypto-detect.json',
                        help='The output JSON file (default: crypto-detect.json).')
    parser.add_argument('--all-hidden', action='store_true', help='Scan all hidden files/folders')
    parser.add_argument('--debug', '-d', action='store_true', help='Enable debug messages')
    parser.add_argument('--quiet', '-q', action='store_true', help='Enable quiet mode')
    parser.add_argument('--trace', '-t', action='store_true', help='Enable trace mode')
    args = parser.parse_args()
    if args.version:
        ver()
        exit(0)
    if not args.target_dir:
        print_stderr('Error: Need to specify target directory to process.')
        parser.print_help()
        exit(1)
    debug = args.debug
    quiet = args.quiet
    trace = args.trace
    all_hidden = args.all_hidden
    return args


def ver():
    """
    Print version information
    """
    print(f'Version: {__version__}')


def main():
    """
    Run the keyword analyser to detect cryptographic algorithms
    """
    args = setup_args()
    if not args:
        exit(1)
    if not run_scan(args.target_dir, args.definitions, args.output):
        exit(1)
    exit(0)


if __name__ == "__main__":
    main()