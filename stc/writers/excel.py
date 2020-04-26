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
    for i in lr(1, len(dataframe.columns)):
        worksheet.set_column(i, i, width)


def set_column_width_by_name(name, width, data_frame, worksheet):
    col_i = data_frame.columns.get_loc(name) + 1
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


def standard_processor_writer(default_width=8, groups=[], **col_width):
    """
    standard writer with autosize column
    """
    def _standard_processor_writer(excel_path, data_frame):
        sheet_name = "data"

        data_frame.index.name = "No."
        data_frame.index = data_frame.index + 1
        # setup index

        writer = get_writer_new_excel(excel_path)
        data_frame.to_excel(
            writer,
            sheet_name=sheet_name,
            startrow=1 if len(groups) > 0 else 0
        )
        worksheet = writer.sheets[sheet_name]
        workbook = writer.book
        # setup xlsxwriter objects and print dataframe

        if len(groups) > 0:
            format = workbook.add_format()
            format.set_bold()
            format.set_border()
            format.set_align('center')
            no_group = lr(0, len(data_frame.columns) - 1)
            lformat = workbook.add_format()
            lformat.set_left()
            rformat = workbook.add_format()
            rformat.set_right()
            for group, start, end in groups:
                worksheet.merge_range(0, start + 1, 0, end + 1,
                                      group, format)
                worksheet.set_column(start + 1, start + 1, cell_format=lformat)
                worksheet.set_column(end + 1, end + 1, cell_format=rformat)
                no_group = [x for x in no_group if x < start or x > end]
            # create group headers
            worksheet.merge_range(0, 0, 1, 0, data_frame.index.name, format)
            # merge index header
            for i in no_group:
                worksheet.merge_range(0, i + 1, 1, i + 1,
                                      data_frame.columns[i], format)
            # merge ungrouped headers
        set_all_column_width(data_frame, worksheet, default_width)
        worksheet.set_column(0, 0, 4)
        if col_width is not None:
            for column in col_width.keys():
                try:
                    set_column_width_by_name(
                        column, col_width[column], data_frame, worksheet
                    )
                except KeyError:
                    pass
        # set column widths

        writer.save()
    return _standard_processor_writer
