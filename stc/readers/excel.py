"""
stc.readers.excel
~~~~~~~~~~~~~~~~~

Read excel files util
"""

import pandas as pd
import functools


def excel_sheet_to_frame(excel_path, sheet, columns):
    full_frame = pd.read_excel(excel_path, sheet_name=sheet)
    return functools.reduce(lambda a, x: a + x, [full_frame.iloc[:, x].astype(str) for x in columns]).str.cat(sep='\n')
