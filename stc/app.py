"""
app
~~~~~~~

Main application initialization
"""

import sys
import re

import logger
import filesys
import proc_loader
from table import make_table
from utils import get_path, join_path, get_basename_from_path

CMD_ARGS = list(sys.argv)

try:
    DIR = CMD_ARGS[1]
except IndexError:
    DIR = get_path("Enter path to directory of data")

try:
    base_name = get_basename_from_path(DIR).replace(' ', '_').lower()
    proc = proc_loader.load_proc(base_name)
    if proc is None:
        raise ModuleNotFoundError
    print(f"successfully loaded processor '{base_name}'")
except ModuleNotFoundError:
    print(f"no processor '{base_name}' defined")
    print(f"make sure your data directory is the same as processor")
    print(f"list of available processors:")
    for p in proc_loader.PROCESSORS:
        print(f"  {p.__name__}")
    sys.exit(1)

# STEP 0 load processor matching data directory

try:
    EXCEL_DIR_PATH = CMD_ARGS[2]
except IndexError:
    EXCEL_DIR_PATH = get_path("Enter path to directory to store excel file")

try:
    FILE_NAME = CMD_ARGS[3]
except IndexError:
    FILE_NAME = input("Enter filename (without extensions):\n  ")

# STEP 1 get user input

EXCEL_PATH = join_path(EXCEL_DIR_PATH, f'{FILE_NAME}.xlsx')
print(f"\nreading file paths in '{DIR}'...")
FILE_PATHS = [join_path(DIR, f) for f in filesys.get_files_from_dir(DIR)]
NUMBER_OF_FILES = len(FILE_PATHS)

# STEP 2 collate file paths


def wrap_log(i, path, reader):
    logger.log_reader(i, NUMBER_OF_FILES, path)
    return reader(path)


FILE_PATH_STR_PAIRS = [
    (p, wrap_log(i, p, proc.READER))
    for i, p in enumerate(FILE_PATHS)
]

if NUMBER_OF_FILES > 0:
    logger.erase_line()

# STEP 3 read files

FAILED_TO_READ_FILES = [p for p, f in FILE_PATH_STR_PAIRS if f is None]
FILE_PATH_STR_PAIRS = [x for x in FILE_PATH_STR_PAIRS if not x[1] is None]
NUMBER_OF_READ_FILES = len(FILE_PATH_STR_PAIRS)
if NUMBER_OF_FILES > NUMBER_OF_READ_FILES:
    logger.log_failed_reads(
        NUMBER_OF_FILES,
        NUMBER_OF_READ_FILES,
        FAILED_TO_READ_FILES
    )

# STEP 4 remove failed to read files

print(f"\nextracting data from {NUMBER_OF_READ_FILES} files...")
DATA_FRAME, ERRORS = make_table(
    proc.SELECTORS,
    FILE_PATH_STR_PAIRS
)

proc.WRITER(EXCEL_PATH, DATA_FRAME)

# STEP 5 generate excel file

if not ERRORS.empty:
    logger.log_errors(ERRORS)

logger.log_success(NUMBER_OF_READ_FILES, NUMBER_OF_FILES, EXCEL_PATH)

# STEP 6 print results
