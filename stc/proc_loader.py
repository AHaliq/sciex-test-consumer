"""
proc_loader
~~~~~~~~~~~

Given directory name loads module for it
"""

import re

import processors.garage_cooler_assembly
import processors.pa800_excel_spreadsheets
import processors.pressure_module


PROCESSORS = [
    processors.garage_cooler_assembly,
    processors.pa800_excel_spreadsheets,
    processors.pressure_module
]


def load_proc(dir_name):
    for p in PROCESSORS:
        if txt_match_proc(p, dir_name):
            return p
    return None


def txt_match_proc(proc, txt):
    proc_txt = proc.__name__.split('.')[1]
    regexp = re.compile(rf'^{proc_txt}.*', flags=re.IGNORECASE)
    if regexp.match(txt):
        return True
    return False
