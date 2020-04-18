"""
stc.app
~~~~~~~

Main application initialization
"""

import sys

import selector.common as ex

from filesys import get_files_from_dir
from writers.excel import write_frame_to_new_excel
from readers.txt import txt_file_to_str

from table import make_table
from utils import get_path, join_path
from processors.garage_cooler_assembly import SELECTORS, FORMATTER

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

FILE_PATHS = [join_path(DIR, f) for f in get_files_from_dir(DIR)]
FILE_PATH_STR_PAIRS = [(p, txt_file_to_str(p)) for p in FILE_PATHS]

print(f"\nextracting data from {len(FILE_PATHS)} files...")
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
    print("\nselector failures:")
    print(ERRORS)
print(f"\nsuccessfully generated '{EXCEL_PATH}'")
