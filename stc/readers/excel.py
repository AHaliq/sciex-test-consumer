"""
stc.readers.excel
~~~~~~~~~~~~~~~~~

Read excel files util
"""

import pandas as pd
import functools
from utils import list_range as lr


def excel_sheet_to_str(excel_path, sheet, columns):
    """
    given path to excel file attempt to read specified sheet at specified column numbers
    """
    full_frame = pd.read_excel(excel_path, sheet_name=sheet)

    def create_column(column):
        rows = full_frame.shape[0]
        if type(column) == str:
            return pd.Series([column for y in lr(rows)])
        return full_frame.iloc[:, column].astype(str)

    return functools.reduce(
        lambda a, x: a + x, [create_column(x) for x in columns]
    ).str.cat(sep='\n')


def replace_none_blank(data_frame):
    mask = data_frame.applymap(lambda x: x is None)
    cols = data_frame.columns[(mask).any()]
    for col in data_frame[cols]:
        data_frame.loc[mask[col], col] = ''
