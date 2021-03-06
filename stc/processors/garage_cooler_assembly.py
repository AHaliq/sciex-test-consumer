"""
processors.garage_cooler_assembly
~~~~~~~

Markup for garage_cooler_assembly dataset
"""

import selector.common as ex
import xlsxwriter

from utils import list_range as lr
from writers.excel import auto_fit_columns, standard_processor_writer
from readers.txt import txt_file_to_str

READER = txt_file_to_str

SELECTORS = [
    ex.name_selector,
    ex.date_selector,
    ex.model_selector,
    ex.serial_selector(),
] + [
    ex.field_selector(row_id=i)
    for i in lr(0, 11) + lr(54, 56) + lr(63, 65)
]

WRITER = standard_processor_writer(
    default_width=12,
    groups=[("Teach I", 4, 6), ("Teach O", 7, 9), ("Teach GI", 10, 12),
            ("Teach GO", 13, 15), ("Offset In", 16, 18), ("Offset Out", 19, 21)],
    date=11,
    name=11,
    model=6,
    serial=5
)
