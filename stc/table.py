"""
table
~~~~~~~~~

Util to generate DataFrames
"""

import pandas as pd
from utils import get_basename_from_path
from selector.common import filename_selector


def make_table(selectors, file_path_str_pairs):
    """
    Generate dataframe
    @param selectors            list of selectors in order; values extracted as columns
                                tuple of selector and column name is accepted as well
    @param file_path_str_pairs  list of pairs of file_path and file_str
    @return pair of dataframe and selector failures
    """
    column_map = {k: None for k in selectors}
    selector_key = 'selectors'
    file_key = 'file_name'
    failures = pd.DataFrame([], columns=[selector_key, file_key])

    def extract(selector_column, file_path_str_pair):
        file_path, file_str = file_path_str_pair
        if type(selector_column) == tuple:
            selector, label = selector_column
        else:
            selector = selector_column
            label = None
        try:
            if selector == filename_selector:
                res = file_path
            else:
                res = selector(file_str)
            if column_map[selector_column] is None:
                if label is not None:
                    column_map[selector_column] = label
                else:
                    column_map[selector_column] = selector(file_str, True)
            return res
        except (AttributeError, IndexError, TypeError):
            nonlocal failures
            new_failure = {}
            new_failure[selector_key] = selector.__name__
            new_failure[file_key] = get_basename_from_path(file_path)
            next_failures = failures.append(new_failure, ignore_index=True)
            failures = next_failures
            return None
    data = [[extract(s, f) for s in selectors] for f in file_path_str_pairs]
    columns = [column_map[s] for s in selectors]
    return pd.DataFrame(data, columns=columns), failures


def errors_to_file_errors(errors, inv=False):
    file_errors = {}
    for index, row in errors.iterrows():
        file_name = row.at['file_name']
        selector_name = row.at['selectors']
        try:
            if inv:
                file_errors[selector_name].append(file_name)
            else:
                file_errors[file_name].append(selector_name)
        except KeyError:
            if inv:
                file_errors[selector_name] = [file_name]
            else:
                file_errors[file_name] = [selector_name]
    return file_errors
