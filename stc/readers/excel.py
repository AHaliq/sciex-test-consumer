"""
stc.readers.excel
~~~~~~~~~~~~~~~~~

Read excel files util
"""

import pandas as pd


def excel_sheet_to_frame(excel_path, sheet):
    full_frame = pd.read_excel(excel_path, sheet_name=sheet)
    return (full_frame.iloc[:, 0].astype(str) + full_frame.iloc[:, 1].astype(str)).str.cat(sep='\n')
