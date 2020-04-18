"""
stc.app
~~~~~~~

Main application initialization
"""

import sys

import selector.common as ex

from filesys import get_files_from_dir
from writers.excel import write_frame_to_new_excel

from table import make_table
from utils import get_path, join_path
from processors.pa800_excel import SELECTORS, FORMATTER, READER

OKBLUE = '\033[94m'
WARNING = '\033[93m'
OKGREEN = '\033[92m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
ENDC = '\033[0m'

CMD_ARGS = list(sys.argv)

try:
    DIR = CMD_ARGS[1]
except IndexError:
    DIR = get_path("Enter path to directory of data")

try:
    EXCEL_DIR_PATH = CMD_ARGS[2]
except IndexError:
    EXCEL_DIR_PATH = get_path("Enter path to directory to store excel file")

try:
    FILE_NAME = CMD_ARGS[3]
except IndexError:
    FILE_NAME = input("Enter filename (without extensions):\n  ")

EXCEL_PATH = join_path(EXCEL_DIR_PATH, f'{FILE_NAME}.xlsx')
print(f"\nreading file paths in '{DIR}'...")
FILE_PATHS = [join_path(DIR, f) for f in get_files_from_dir(DIR)]
NUMBER_OF_FILES = len(FILE_PATHS)


def log_reader(i, path):
    sys.stdout.write('\x1b[2K')
    print(
        f"{OKBLUE}[{i + 1}/{NUMBER_OF_FILES}]{ENDC} reading '{path}'",
        end='\r'
    )
    return READER(path)


FILE_PATH_STR_PAIRS = [(p, log_reader(i, p)) for i, p in enumerate(FILE_PATHS)]

if NUMBER_OF_FILES > 0:
    sys.stdout.write('\x1b[2K')

FAILED_TO_READ_FILES = [p for p, f in FILE_PATH_STR_PAIRS if f is None]
FILE_PATH_STR_PAIRS = [x for x in FILE_PATH_STR_PAIRS if not x[1] is None]
NUMBER_OF_READ_FILES = len(FILE_PATH_STR_PAIRS)
if NUMBER_OF_FILES > NUMBER_OF_READ_FILES:
    print(f'{WARNING}{BOLD}failed to read {NUMBER_OF_FILES - NUMBER_OF_READ_FILES} files{ENDC}')
    for f in FAILED_TO_READ_FILES:
        print(f'  {WARNING}{f}{ENDC}')

print(f"\nextracting data from {NUMBER_OF_READ_FILES} files...")
DATA_FRAME, ERRORS = make_table(
    SELECTORS,
    FILE_PATH_STR_PAIRS
)

write_frame_to_new_excel(
    EXCEL_PATH,
    DATA_FRAME,
    format_func=FORMATTER(DATA_FRAME)
)

if not ERRORS.empty:
    print(WARNING + BOLD + "\ntabulating selector failures..." + ENDC)
    file_errors = {}
    for index, row in ERRORS.iterrows():
        file_name = row.at['file_name']
        selector_name = row.at['selectors']
        try:
            file_errors[file_name].append(selector_name)
        except KeyError:
            file_errors[file_name] = [selector_name]
    print(WARNING + BOLD + "\nselector failures:" + ENDC)
    error_list = file_errors.items()
    fail_count = 0
    for key, value in error_list:
        print(WARNING + UNDERLINE + key + ENDC)
        for selector in value:
            fail_count += 1
            print(WARNING + f'  {selector}' + ENDC)
    print(WARNING + BOLD +
          f"\n{len(error_list)} files has {fail_count} selector failures:" + ENDC)

print(f"\n{OKGREEN}{NUMBER_OF_READ_FILES} out of {NUMBER_OF_FILES} files successfully generated '{EXCEL_PATH}'{ENDC}")
# TODO improve error listing; filename: selectors,...
