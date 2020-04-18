"""
Markup for garage_cooler_assembly dataset
"""

import selector.common as ex
import xlsxwriter

from utils import list_range as lr
from writers.excel import auto_fit_columns
from readers.txt import txt_file_to_str

READER = txt_file_to_str

SELECTORS = [
    ex.name_selector,
    ex.date_selector,
    ex.model_selector,
    ex.serial_selector
] + [
    ex.field_selector(row_id=i)
    for i in lr(0, 11) + lr(54, 56) + lr(63, 65)
]


def FORMATTER(data_frame):
    def _FORMATTER(worksheet: xlsxwriter.worksheet.Worksheet):
        auto_fit_columns(data_frame, worksheet)
    return _FORMATTER
