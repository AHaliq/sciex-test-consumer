"""
stc.selector.common
~~~~~~~~~~~~~~~~~~~~

Common extractors between different test data types
"""

import re


def name_selector(file_str, label=None):
    regexp = re.compile(r"Name: (.+)\n")
    return regexp.search(file_str).group(1).strip() if label is None else "name"


def model_selector(file_str, label=None):
    regexp = re.compile(r"Instrument Model: (.+)SN: (.+)\n")
    return regexp.search(file_str).group(1).strip() if label is None else "model"


def serial_selector(file_str, label=None):
    regexp = re.compile(r"Instrument Model: (.+)SN: (.+)\n")
    return regexp.search(file_str).group(2).strip() if label is None else "serial"


def field_selector(field_name='.*', row_id='.*', data_type='.*'):
    def selector(file_str, label=None):
        regexp = re.compile(
            rf"\n({field_name})\s+\[({row_id})\]\s+(=*)\s*(.*)\s+\(({data_type})\).*\n")
        match = regexp.search(file_str)
        return match.group(4).strip() if label is None else (None if match is None else match.group(1).strip())
    return selector
