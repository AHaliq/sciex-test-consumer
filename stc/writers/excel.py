"""
stc.writers.excel
~~~~~~~~~~~~~~~~~

Write utility to excel files
"""

import pandas as pd


def write_frame_to_new_excel(path, file_name, frame):
    writer = pd.ExcelWriter(f'{path}/{file_name}.xlsx', engine='xlsxwriter')
    frame.to_excel(writer, sheet_name='Sheet1')
    writer.save()
