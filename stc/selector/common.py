"""
stc.selector.common
~~~~~~~~~~~~~~~~~~~~

Common extractors between different test data types
"""

import re
import pandas as pd
from utils import regexp_space_between as sb, month_dict

# regexp constants
_NAME = sb('name')
_INSTRUMENT = sb('instrument')
_ABBR_INSTRUMENT = sb('instrmnt.')
_DATE = sb('date')
_MODEL = sb('model')
_EEPROM = sb('eeprom')
_SN = r's/?n'


def name_selector(file_str, label=None):
    """
    selects name

    the following formats are accepted:

    NAME: <name>

    capture ends with: optionally instrument and model
    """
    regexp = re.compile(
        rf"{_NAME}:\s*(.+)\s*({_INSTRUMENT}|{_ABBR_INSTRUMENT})?({_MODEL})",
        flags=re.IGNORECASE
    )
    return regexp.search(file_str).group(1).strip() if label is None else "name"


def model_selector(file_str, label=None):
    """
    selects model where the word instrument is optional

    the following formats are accepted:

    MODEL: <model>
    MODEL/SN: <model>/...
    MODEL/S/N: <model>/...

    capture ends with: instrument or serial
    """
    try:
        regexp = re.compile(
            rf"{_MODEL}\s*:\s*(.*?)\+?\s*({_INSTRUMENT}|{_ABBR_INSTRUMENT}|{_SN})",
            flags=re.IGNORECASE
        )
        return regexp.search(file_str).group(1).strip() if label is None else "model"
    except (AttributeError, IndexError):
        regexp = re.compile(
            rf"{_MODEL}/{_SN}\s*:\s*(.*?)\+?(/| )",
            flags=re.IGNORECASE
        )
        return regexp.search(file_str).group(1).strip() if label is None else "model"


def serial_selector(file_str, label=None):
    """
    selects serial number and takes last 4 characters

    the following formats are accepted:

    S/N: <serial>
    SN: <serial>
    MODEL/SN: .../<serial>
    MODEL/S/N: .../<serial>

    capture ends with: date, eeprom, dashed border, >
    """
    def actual(file_str, label=None):
        try:
            regexp = re.compile(
                rf"/\s*{_SN}\s*:\s*(.*?)(/| )/?(.*?)((A|B).*)\s*({_DATE}|{_EEPROM}|-|>)",
                flags=re.IGNORECASE
            )
            return regexp.search(file_str).group(4).strip() if label is None else "serial"
        except (AttributeError, IndexError):
            regexp = re.compile(
                rf"{_SN}\s*:\s*(.*)\s*({_DATE}|{_EEPROM}|-|>)",
                flags=re.IGNORECASE
            )
            return regexp.search(file_str).group(1).strip() if label is None else "serial"
    if label is None:
        return actual(file_str)[-4:]
    return actual(file_str, label)


def date_selector(file_str, label=None):
    """
    selects the date value and converts to pandas timeframe

    the following formats are accepted:

    DATE: <two digit day> <three character month> <4 digit year>
    """
    regexp = re.compile(
        r"([0-9]{2})(th|st|nd)?\s*([a-z]{3})\s*([0-9]{4})",
        flags=re.IGNORECASE
    )
    match = regexp.search(file_str)
    day = int(match.group(1))
    month = int(month_dict(match.group(3)))
    year = int(match.group(4))
    return pd.Timestamp(year=year, month=month, day=day) if label is None else "date"


def field_selector(field_name='.*', row_id='.*', data_type='.*'):
    """
    selects a field with the argument regexp

    the following formats are accepted

    <field> [<id>] [=] <data> <data_type> <remarks>

    capture ends with: newline or EOF
    """
    def selector(file_str, label=None):
        regexp = re.compile(
            rf"\n({field_name})\s+\[({row_id})\]\s+(=*)\s*(.*)\s+\(({data_type})\).*(\n|\Z)",
            flags=re.IGNORECASE)
        match = regexp.search(file_str)
        field_value = None if match is None else match.group(1).strip()
        return match.group(4).strip() if label is None else field_value
    return selector
