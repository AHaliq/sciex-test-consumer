"""
stc.selector.common
~~~~~~~~~~~~~~~~~~~~

Common extractors between different test data types
"""

import re
import pandas as pd
from utils import regex_space_between as sb, MNTH_DICT

NAME = sb('name')
INSTRUMENT = sb('instrument')
ABBR_INSTRUMENT = sb('instrmnt.')
DATE = sb('date')
MODEL = sb('model')
EEPROM = sb('eeprom')
SN = r's/?n'


def name_selector(file_str, label=None):
    regexp = re.compile(
        rf"{NAME}:\s*(.+)\s*({INSTRUMENT}|{ABBR_INSTRUMENT})?({MODEL})", flags=re.IGNORECASE
    )
    return regexp.search(file_str).group(1).strip() if label is None else "name"


def model_selector(file_str, label=None):
    try:
        regexp = re.compile(
            rf"{MODEL}\s*:\s*(.*?)\+?\s*({INSTRUMENT}|{ABBR_INSTRUMENT}|{SN})", flags=re.IGNORECASE
        )
        return regexp.search(file_str).group(1).strip() if label is None else "model"
    except (AttributeError, IndexError):
        regexp = re.compile(
            rf"({INSTRUMENT}|{ABBR_INSTRUMENT})?{MODEL}/{SN}\s*:\s*(.*?)\+?(/| )", flags=re.IGNORECASE
        )
        return regexp.search(file_str).group(2).strip() if label is None else "model"


def serial_selector(file_str, label=None):
    def actual(file_str, label=None):
        try:
            regexp = re.compile(
                rf"/\s*{SN}\s*:\s*(.*?)(/| )/?(.*?)((A|B).*)\s*({DATE}|{EEPROM}|-|>)", flags=re.IGNORECASE
            )
            return regexp.search(file_str).group(4).strip() if label is None else "serial"
        except (AttributeError, IndexError):
            regexp = re.compile(
                rf"{SN}\s*:\s*(.*)\s*({DATE}|{EEPROM}|-|>)", flags=re.IGNORECASE
            )
            return regexp.search(file_str).group(1).strip() if label is None else "serial"
    if label is None:
        return actual(file_str)[-4:]
    return actual(file_str, label)


def date_selector(file_str, label=None):
    regexp = re.compile(
        r"([0-9]{2})(th|st|nd)?\s*([a-z]{3})\s*([0-9]{4})", flags=re.IGNORECASE
    )
    match = regexp.search(file_str)
    day = int(match.group(1))
    month = int(MNTH_DICT[match.group(3).lower().capitalize()])
    year = int(match.group(4))
    return pd.Timestamp(year=year, month=month, day=day) if label is None else "date"


def field_selector(field_name='.*', row_id='.*', data_type='.*'):
    def selector(file_str, label=None):
        regexp = re.compile(
            rf"\n({field_name})\s+\[({row_id})\]\s+(=*)\s*(.*)\s+\(({data_type})\).*(\n|\Z)", flags=re.IGNORECASE)
        match = regexp.search(file_str)
        return match.group(4).strip() if label is None else (None if match is None else match.group(1).strip())
    return selector
