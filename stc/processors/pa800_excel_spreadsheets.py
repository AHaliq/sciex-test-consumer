"""
processors.p800_excel_spreadsheets
~~~~~~~

Markup for p800 dataset
"""

import selector.common as ex
import selector.pa800_excel_spreadsheets as ex8
import xlsxwriter

from utils import list_range as lr, flatten
from writers.excel import auto_fit_columns, standard_processor_writer
from readers.excel import excel_sheet_to_str
import xlrd


def READER(file_path):
    try:
        eeprom = excel_sheet_to_str(file_path, 'Final EEPROM', [0, 1])
        chemistry = excel_sheet_to_str(file_path, "Chemistry", (1, 2, ">>", 3))
        return eeprom + '\n##CHEMISTRY##\n' + chemistry
    except xlrd.biffh.XLRDError:
        return None


SELECTORS = [
    ex.name_selector,
    ex.date_selector,
    ex.constant_selector("PA800", "model"),
    ex.serial_selector()
] + [
    ex.field_selector(row_id=i)
    for i in lr(0, 11) + lr(54, 56) + lr(63, 65)
] + flatten([
    [
        ex8.run_area_selector(i),
        ex8.run_migration_selector(i),
    ]
    for i in lr(1, 6)
])

WRITER = standard_processor_writer(default_width=12, date=11, name=11)
