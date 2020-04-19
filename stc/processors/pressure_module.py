"""
processors.pressure_module
~~~~~~~

Markup for pressure module dataset
"""

import selector.common as ex
import selector.pressure_module as expm
import xlsxwriter

from utils import list_range as lr
from writers.excel import auto_fit_columns, standard_processor_writer
from readers.txt import txt_file_to_str
from utils import list_range as lr, flatten

READER = txt_file_to_str

SELECTORS = [
    ex.date_selector,
    ex.serial_selector(False),
] + flatten(
    [
        [
            expm.psi_extractor(
                f'Reference Pressure at {psi} psi', f'ref_{psi}_psi'),
            expm.psi_extractor(
                f'UUT Pressure at {psi} psi', f'uut_{psi}_psi'),
        ] for psi in [0.5, 4.5, 10, 90]
    ]
)

WRITER = standard_processor_writer
