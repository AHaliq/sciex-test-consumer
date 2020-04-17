"""
stc.writers.excel
~~~~~~~~~~~~~~~~~

Write utility to excel files
"""

import pandas as pd


def write_frame_to_new_excel(path, file_name, frame):
    with pd.ExcelWriter(f'{path}/{file_name}.xlsx', engine='xlsxwriter') as xl_writer:  # pylint: disable=abstract-class-instantiated
        frame.to_excel(xl_writer, sheet_name='Sheet1')
        xl_writer.save()
