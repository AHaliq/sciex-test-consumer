"""
stc.table
~~~~~~~~~

Util to generate DataFrames
"""

import pandas as pd
from utils import get_file_from_path


def make_table(selectors, file_path_str_pairs):
    print('start to make table')
    column_map = {k: None for k in selectors}
    selector_key = 'selectors'
    file_key = 'file_name'
    failures = pd.DataFrame([], columns=[selector_key, file_key])

    def extract(selector, file_path_str_pair):
        file_path, file_str = file_path_str_pair
        try:
            res = selector(file_str)
            if column_map[selector] is None:
                column_map[selector] = selector(file_str, True)
            return res
        except (AttributeError, IndexError):
            # TODO print missing data based on selector
            nonlocal failures
            new_failure = {}
            new_failure[selector_key] = selector.__name__
            new_failure[file_key] = get_file_from_path(file_path)
            failures = failures.append(new_failure, ignore_index=True)
            return None
    data = [[extract(s, f) for s in selectors] for f in file_path_str_pairs]
    columns = [column_map[s] for s in selectors]
    return pd.DataFrame(data, columns=columns), failures
