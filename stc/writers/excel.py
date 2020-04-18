"""
stc.writers.excel
~~~~~~~~~~~~~~~~~

Write utility to excel files
"""

import pandas as pd


def auto_fit_columns(dataframe, worksheet):
    """
    formatter util to autosize columns
    """
    def get_col_widths(dataframe):
        idx_max = max(
            [len(str(s)) for s in dataframe.index.values] + [len(str(dataframe.index.name))])
        return [idx_max] + [max([len(str(s)) for s in dataframe[col].values] + [len(col)]) for col in dataframe.columns]
    for i, width in enumerate(get_col_widths(dataframe)):
        worksheet.set_column(i, i, width)


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


def standard_processor_writer(excel_path, data_frame):
    """
    standard writer with autosize column
    """
    sheet_name = "data"
    writer = get_writer_new_excel(excel_path)
    data_frame.to_excel(writer, sheet_name=sheet_name)
    auto_fit_columns(data_frame, writer.sheets[sheet_name])
    writer.save()
