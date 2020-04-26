"""
writers.excel
~~~~~~~~~~~~~~~~~

Write utility to excel files
"""

import pandas as pd
from operator import itemgetter
from utils import list_range as lr


def auto_fit_columns(dataframe, worksheet):
    """
    formatter util to autosize columns
    """
    def get_col_widths(dataframe):
        idx_max = max(
            [len(str(s)) for s in dataframe.index.values] + [len(str(dataframe.index.name))])
        return [idx_max] + [max([len(str(s)) for s in dataframe[col].values] + [len(str(col))]) for col in dataframe.columns]
    for i, width in enumerate(get_col_widths(dataframe)):
        worksheet.set_column(i, i, width)


def set_all_column_width(dataframe, worksheet, width):
    for i in lr(0, len(dataframe.columns) - 1):
        worksheet.set_column(i, i, width)


def set_column_width_by_name(name, width, data_frame, worksheet):
    col_i = data_frame.columns.get_loc(name)
    worksheet.set_column(col_i, col_i, width)


def get_writer_new_excel(file_path):
    """
    given a path to an excel file, create an xlsxwriter object
    """
    return pd.ExcelWriter(
        path=file_path,
        engine='xlsxwriter',
        datetime_format='dd/mm/yyyy',
        options={
            "strings_to_numbers": True,
        }  # pylint: disable=abstract-class-instantiated
    )


def standard_processor_writer(default_width=8, **col_width):
    """
    standard writer with autosize column
    """
    def _standard_processor_writer(excel_path, data_frame):
        sheet_name = "data"
        writer = get_writer_new_excel(excel_path)
        data_frame.to_excel(writer, sheet_name=sheet_name, index=False)
        worksheet = writer.sheets[sheet_name]
        set_all_column_width(data_frame, worksheet, default_width)
        if col_width is not None:
            for column in col_width.keys():
                try:
                    set_column_width_by_name(
                        column,
                        col_width[column],
                        data_frame,
                        worksheet
                    )
                except KeyError:
                    pass
        writer.save()
    return _standard_processor_writer
