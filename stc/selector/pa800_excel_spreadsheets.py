"""
selector.pa800_excel_spreadsheets
~~~~~~~~~~~~~~~~~~~~

Common extractors between for dataset pa800
"""

import re

_DIVIDER = r"##CHEMISTRY##.*?"


def run_area_selector(id):
    """
    selects run area

    the following formats are accepted:

    run<id>x.xxy.yy

    capture ends with: optionally instrument and model
    """
    def _run_area_selector(file_str, label=None):
        regexp = re.compile(
            rf"{_DIVIDER}run{id}([0-9]+(\.[0-9]+)?)>>",
            flags=re.IGNORECASE | re.DOTALL
        )
        return regexp.search(file_str).group(1) if label is None else f"run{id} area"
    _run_area_selector.__name__ = f"run{id}_area_selector"
    return _run_area_selector


def run_migration_selector(id):
    """
    selects run area

    the following formats are accepted:

    run<id>x.xxy.yy

    capture ends with: optionally instrument and model
    """
    def _run_migration_selector(file_str, label=None):
        regexp = re.compile(
            rf"{_DIVIDER}run{id}.*?>>([0-9]+(\.[0-9]+)?)",
            flags=re.IGNORECASE | re.DOTALL
        )
        return regexp.search(file_str).group(1) if label is None else f"run{id} migration"
    _run_migration_selector.__name__ = f"run{id}_migration_selector"
    return _run_migration_selector
