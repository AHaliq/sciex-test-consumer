"""
stc.writers.excel
~~~~~~~~~~~~~~~~~

Write utility to excel files
"""

import pandas as pd


def write_frame_to_new_excel(file_path, dataframe, sheet_name='data', format_func=None):
    """
    Given a path to output, file_name to write and dataframe, write the excel file
    """
    writer = get_writer_new_excel(file_path)
    dataframe.to_excel(writer, sheet_name=sheet_name)
    if not format_func is None:
        format_func(writer.sheets[sheet_name])
    writer.save()
    return writer


def auto_fit_columns(dataframe, worksheet):
    def get_col_widths(dataframe):
        idx_max = max(
            [len(str(s)) for s in dataframe.index.values] + [len(str(dataframe.index.name))])
        return [idx_max] + [max([len(str(s)) for s in dataframe[col].values] + [len(col)]) for col in dataframe.columns]
    for i, width in enumerate(get_col_widths(dataframe)):
        worksheet.set_column(i, i, width)


def get_writer_new_excel(file_path):
    return pd.ExcelWriter(
        path=file_path,
        engine='xlsxwriter',
        datetime_format='dd/mm/yyyy',
        options={
            "strings_to_numbers": True,
        }  # pylint: disable=abstract-class-instantiated
    )
