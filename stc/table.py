"""
stc.table
~~~~~~~~~

Util to generate DataFrames
"""

import pandas as pd


def make_table(selectors, file_strs):
    column_map = {k: None for k in selectors}

    def extract(selector, file_str):
        try:
            res = selector(file_str)
            if column_map[selector] is None:
                column_map[selector] = selector(file_str, True)
            return res
        except (AttributeError, IndexError):
            # TODO print missing data based on selector
            print("ERROR---")
            print('\n'.join(file_str.split('\n')[0:5]))
            print("--------")
            return None
    data = [[extract(s, f) for s in selectors] for f in file_strs]
    columns = [column_map[s] for s in selectors]
    return pd.DataFrame(data, columns=columns)
