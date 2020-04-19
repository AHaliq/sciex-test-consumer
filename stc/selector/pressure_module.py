"""
selector.pressure_module
~~~~~~~~~~~~~~~~~~~~

Common extractors between for pressure module
"""

import re

import selector.common as ex


def psi_extractor(key, column_name=None):
    actual_selector = ex.key_value_selector(
        key, r'[0-9]+\.[0-9]+ psi', column_name)

    def _wrapper(file_str, label=None):
        res = actual_selector(file_str, label)
        if label is None:
            regexp = re.compile(rf'(.*?)\s*psi', flags=re.IGNORECASE)
            return regexp.match(res).group(1)
        return res
    _wrapper.__name__ = actual_selector.__name__
    return _wrapper
