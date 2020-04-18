"""
Markup for garage_cooler_assembly dataset
"""

import selector.common as ex
import xlsxwriter

from utils import list_range as lr
from writers.excel import auto_fit_columns
from readers.excel import excel_sheet_to_frame
import xlrd


def READER(file_path):
    try:
        return excel_sheet_to_frame(file_path, 'Final EEPROM', [0, 1])
    except xlrd.biffh.XLRDError:
        return None


SELECTORS = [
    ex.name_selector,
    ex.date_selector,
    ex.constant_selector("PA800", "model"),
    ex.serial_selector
] + [
    ex.field_selector(row_id=i)
    for i in lr(0, 11) + lr(54, 56) + lr(63, 65)
]


def FORMATTER(data_frame):
    def _FORMATTER(worksheet: xlsxwriter.worksheet.Worksheet):
        auto_fit_columns(data_frame, worksheet)
    return _FORMATTER
