#!/usr/local/bin/python3
"""
stc.app
~~~~~~~

Main application initialization
"""

import sys

import selector.common as ex

from filesys import get_files_from_dir
from writers.excel import write_frame_to_new_excel
from readers.txt import txt_to_str

from table import make_table
from utils import lr, getPath, evalPath, regex_space_between

CMD_ARGS = list(sys.argv)

try:
    DIR = CMD_ARGS[1]
except IndexError as error:
    DIR = getPath("Enter path to directory of data")

FILE_STRS = [txt_to_str(f'{DIR}/{f}') for f in get_files_from_dir(DIR)]
SELECTORS = [
    ex.name_selector,
    ex.date_selector,
    ex.model_selector,
    ex.serial_selector
] + [ex.field_selector(row_id=i) for i in lr(0, 11) + lr(54, 56) + lr(63, 65)]

DATA_FRAME = make_table(SELECTORS, FILE_STRS)

write_frame_to_new_excel(
    # getPath("Enter path to directory to store excel file"),
    evalPath("~/Desktop"),
    "test",  # input("Enter filename (without extensions):\n  "),
    DATA_FRAME)
