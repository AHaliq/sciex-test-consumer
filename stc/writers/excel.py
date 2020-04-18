"""
stc.writers.excel
~~~~~~~~~~~~~~~~~

Write utility to excel files
"""

import os
import pandas as pd

from utils import join_path


def write_frame_to_new_excel(path, file_name, frame):
    """
    Given a path to output, file_name to write and dataframe, write the excel file
    """
    output_path = join_path(path, f'{file_name}.xlsx')
    with pd.ExcelWriter(output_path, engine='xlsxwriter') as xl_writer:  # pylint: disable=abstract-class-instantiated
        frame.to_excel(xl_writer, sheet_name='Sheet1')
        xl_writer.save()
