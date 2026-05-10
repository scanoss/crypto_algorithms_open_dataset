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

__version__ = '0.0.2'
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


def load_algorithm_metadata(spdx_yaml_dir: str) -> dict:
    """
    Load algorithm metadata from the SPDX cryptographic-algorithm-list submodule.

    :param spdx_yaml_dir: path to external/spdx-crypto/yaml
    :return: dictionary of algorithm metadata indexed by algorithm id
    """
    if not os.path.exists(spdx_yaml_dir):
        print_stderr(
            f'Warning: SPDX yaml folder not found at {spdx_yaml_dir}. '
            f'Run "git submodule update --init --recursive". '
            f'Continuing with empty metadata.'
        )
        return {}

    algorithm_metadata = {}
    for file in os.listdir(spdx_yaml_dir):
        if not (file.endswith('.yaml') or file.endswith('.yml')):
            continue
        file_path = os.path.join(spdx_yaml_dir, file)
        print_trace(f'Loading SPDX metadata: {file_path}')
        try:
            with open(file_path, 'r') as yaml_file:
                data = yaml.safe_load(yaml_file) or {}
            if 'id' in data:
                algorithm_metadata[data['id']] = {
                    'algorithm': data.get('name', ''),
                    'category': data.get('cryptoClass', ''),
                    'strength': data.get('commonkeySize', ''),
                }
        except Exception as e:
            print_stderr(f'Error loading SPDX metadata file {file_path}: {e}')
    return algorithm_metadata


def load_definitions(definitions_dir: str) -> tuple:
    """
    Load keyword YAML files from <definitions_dir>/keywords/ and algorithm metadata
    from <definitions_dir>/external/spdx-crypto/yaml/.

    :param definitions_dir: repository root containing keywords/ and external/spdx-crypto/
    :return: tuple of (keyword_definitions, algorithm_metadata, algorithm_map)
    """
    if not definitions_dir or not os.path.exists(definitions_dir):
        print_stderr(f'Error: No definition folder specified, or it does not exist: {definitions_dir}')
        return None, None, None

    spdx_yaml_dir = os.path.join(definitions_dir, 'external', 'spdx-crypto', 'yaml')
    algorithm_metadata = load_algorithm_metadata(spdx_yaml_dir)
    print_debug(f'Loaded {len(algorithm_metadata)} algorithm metadata entries from SPDX')

    keywords_dir = os.path.join(definitions_dir, 'keywords')
    if not os.path.exists(keywords_dir):
        print_stderr(f'Error: keywords folder does not exist: {keywords_dir}')
        return None, None, None

    keyword_definitions = defaultdict(list)
    algorithm_map = {}

    for file in os.listdir(keywords_dir):
        if not (file.endswith('.yaml') or file.endswith('.yml')):
            continue
        file_path = os.path.join(keywords_dir, file)
        print_trace(f'Loading definition: {file_path}')
        try:
            with open(file_path, 'r') as yaml_file:
                data = yaml.safe_load(yaml_file) or {}
            if 'algorithmId' in data and 'keywords' in data:
                algorithm_id = data['algorithmId']
                algorithm_map[file] = algorithm_id
                for keyword in data['keywords']:
                    keyword_definitions[str(keyword)].append({
                        'file': file,
                        'algorithmId': algorithm_id,
                    })
        except Exception as e:
            print_stderr(f'Error loading definition file {file_path}: {e}')

    return keyword_definitions, algorithm_metadata, algorithm_map


def analyse_file(file_path: str, definitions: dict, algorithm_metadata: dict) -> dict:
    """
    Analyse the given file for the specified definitions

    :param file_path: File to analyse
    :param definitions: keyword definitions to search for
    :param algorithm_metadata: metadata for algorithms
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
            for keyword, matches in definitions.items():
                keyword_str = str(keyword)
                if keyword_str in content_str:
                    match_info = []
                    for match in matches:
                        algorithm_id = match.get('algorithmId')
                        match_data = {
                            'def_file': match.get('file'),
                            'algorithmId': algorithm_id
                        }
                        
                        # Add metadata if available
                        if algorithm_id in algorithm_metadata:
                            match_data.update({
                                'algorithm': algorithm_metadata[algorithm_id].get('algorithm', ''),
                                'category': algorithm_metadata[algorithm_id].get('category', ''),
                                'strength': algorithm_metadata[algorithm_id].get('strength', '')
                            })
                        
                        match_info.append(match_data)
                    
                    detections.append({
                        'keyword': keyword_str,
                        'matches': match_info
                    })
    
    return detections


def analyse_directory(target_dir: str, definitions: dict, algorithm_metadata: dict) -> list:
    """
    Analyse the given folder for the specified definitions

    :param target_dir: Target folder to scan
    :param definitions: Keyword definitions to search for
    :param algorithm_metadata: Metadata for algorithms
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
            
            detections = analyse_file(file_path, definitions, algorithm_metadata)
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
    
    # Load the crypto definitions and algorithm metadata
    definitions, algorithm_metadata, algorithm_map = load_definitions(def_dir)
    if not definitions:
        print_stderr(f'Error: Failed to load definitions for: {def_dir}')
        return False
    
    print_debug(f'Loaded {len(definitions)} keyword definitions')
    print_debug(f'Loaded {len(algorithm_metadata)} algorithm metadata entries')
    
    detections = analyse_directory(target_dir, definitions, algorithm_metadata)
    if detections:
        print_msg(f'Writing output to: {output}')
        results = {
            'files': detections,
            'metadata': {
                'total_files': len(detections)
            }
        }
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
    parser.add_argument('--definitions', '-c', type=str, default='.',
                        help='Repository root containing keywords/ and external/spdx-crypto/ (default: .)')
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