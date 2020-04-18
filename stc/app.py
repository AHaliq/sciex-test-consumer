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
from utils import list_range as lr, get_path, join_path

CMD_ARGS = list(sys.argv)

try:
    DIR = CMD_ARGS[1]
except IndexError:
    DIR = get_path("Enter path to directory of data")

try:
    EXCEL_PATH = CMD_ARGS[2]
except IndexError:
    EXCEL_PATH = get_path("Enter path to directory to store excel file")

try:
    FILE_NAME = CMD_ARGS[3]
except IndexError:
    FILE_NAME = input("Enter filename (without extensions):\n  ")

FILE_PATHS = [join_path(DIR, f) for f in get_files_from_dir(DIR)]
FILE_PATH_STR_PAIRS = [(p, txt_file_to_str(p)) for p in FILE_PATHS]

SELECTORS = [
    ex.name_selector,
    ex.date_selector,
    ex.model_selector,
    ex.serial_selector
] + [
    ex.field_selector(row_id=i)
    for i in lr(0, 11) + lr(54, 56) + lr(63, 65)
]

DATA_FRAME, ERRORS = make_table(SELECTORS, FILE_PATH_STR_PAIRS)


write_frame_to_new_excel(EXCEL_PATH, FILE_NAME, DATA_FRAME)

print("\n generated table:")
print(DATA_FRAME)
print("\n selector failures:")
print(ERRORS)
print(f"\n successfully generated '{FILE_NAME}' at '{EXCEL_PATH}'")
