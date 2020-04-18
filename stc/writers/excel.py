"""
stc.writers.excel
~~~~~~~~~~~~~~~~~

Write utility to excel files
"""

import os
import pandas as pd

from utils import join_path


def write_frame_to_new_excel(file_path, frame):
    """
    Given a path to output, file_name to write and dataframe, write the excel file
    """
    with pd.ExcelWriter(file_path, engine='xlsxwriter') as xl_writer:  # pylint: disable=abstract-class-instantiated
        frame.to_excel(xl_writer, sheet_name='Sheet1')
        xl_writer.save()
