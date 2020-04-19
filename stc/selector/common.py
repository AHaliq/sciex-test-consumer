"""
selector.common
~~~~~~~~~~~~~~~~~~~~

Common extractors between different test data types
"""

import re
import pandas as pd
from utils import regexp_space_between as sb, month_dict

# regexp constants
_NAME = sb('name')
_TECHNICIAN = sb('technician')
_INSTRUMENT = sb('instrument')
_ABBR_INSTRUMENT = sb('instrmnt.')
_DATE = sb('date')
_MODEL = sb('model')
_EEPROM = sb('eeprom')
_SN = r's/?n\s*'


def filename_selector(file_str, label=None):
    return "filename"


def constant_selector(fix_value, fix_label):
    """
    Returns fix_value regardless of file_str
    """
    def _constant_selector(file_str, label=None):
        return fix_value if label is None else fix_label
    return _constant_selector


def name_selector(file_str, label=None):
    """
    selects name

    the following formats are accepted:

    NAME: <name>

    capture ends with: optionally instrument and model
    """
    regexp = re.compile(
        rf"({_NAME}|{_TECHNICIAN}):\s*(.+?)\s*(({_INSTRUMENT}|{_ABBR_INSTRUMENT})?{_MODEL}|\n)",
        flags=re.IGNORECASE
    )
    return regexp.search(file_str).group(2).strip().lower().title() if label is None else "name"


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
            rf"{_MODEL}:\s*(.*?)\+?\s*({_INSTRUMENT}|{_ABBR_INSTRUMENT}|{_SN}|\n)",
            flags=re.IGNORECASE
        )
        return regexp.search(file_str).group(1).strip() if label is None else "model"
    except (AttributeError, IndexError):
        regexp = re.compile(
            rf"{_MODEL}/{_SN}:\s*(.*?)\+?(/| )",
            flags=re.IGNORECASE
        )
        return regexp.search(file_str).group(1).strip() if label is None else "model"


def serial_selector(trunc=True):
    def wrapper(file_str, label=None):
        """
        selects serial number and takes last 4 characters

        the following formats are accepted:

        S/N: <serial>
        SN: <serial>
        MODEL/SN: .../<serial>
        MODEL/S/N: .../<serial>

        capture ends with: date, eeprom, dashed border, >
        """
        def _serial_selector(file_str, label=None):
            try:
                regexp = re.compile(
                    rf"/\s*{_SN}:\s*(.*?)(/| )/?(.*?)((A|B).*)\s*({_DATE}|{_EEPROM}|-|>|\n)",
                    flags=re.IGNORECASE
                )
                return regexp.search(file_str).group(4).strip() if label is None else "serial"
            except (AttributeError, IndexError):
                pass
            try:
                regexp = re.compile(
                    rf"{_SN}:\s*(.*)\s*({_DATE}|{_EEPROM}|-|>|\n)",
                    flags=re.IGNORECASE
                )
                return regexp.search(file_str).group(1).strip() if label is None else "serial"
            except (AttributeError, IndexError):
                regexp = re.compile(
                    rf"serial number\s*:\s*(.*)\s*({_DATE}|{_EEPROM}|-|>|\n)",
                    flags=re.IGNORECASE
                )
                return regexp.search(file_str).group(1).strip() if label is None else "serial"

        if label is None:
            result = _serial_selector(file_str)
            if trunc:
                return result[-4:]
            return result
        return _serial_selector(file_str, label)
    wrapper.__name__ = 'serial_selector'
    return wrapper


def date_selector(file_str, label=None):
    """
    selects the date value and converts to pandas timeframe

    the following formats are accepted:

    dd mmm yyyy
    yyyy-mm-dd
    dd/mm/yyyy
    """
    try:
        regexp = re.compile(
            r"([0-9]{2})(th|st|nd)?\s*([a-z]{3})\s*([0-9]{4})",
            flags=re.IGNORECASE
        )
        match = regexp.search(file_str)
        day = int(match.group(1))
        month = int(month_dict(match.group(3)))
        year = int(match.group(4))
        return pd.Timestamp(year=year, month=month, day=day) if label is None else "date"
    except (AttributeError, IndexError, TypeError):
        pass
    try:
        regexp = re.compile(
            r"([0-9]{4})(/|-)([0-9]{1,2})(/|-)([0-9]{1,2})",
            flags=re.IGNORECASE
        )
        match = regexp.search(file_str)
        day = int(match.group(5))
        month = int(match.group(3))
        year = int(match.group(1))
        return pd.Timestamp(year=year, month=month, day=day) if label is None else "date"
    except (AttributeError, IndexError, TypeError):
        regexp = re.compile(
            r"([0-9]{1,2})(/|-)([0-9]{1,2})(/|-)([0-9]{4})",
            flags=re.IGNORECASE
        )
        match = regexp.search(file_str)
        day = int(match.group(3))
        month = int(match.group(1))
        year = int(match.group(5))
        return pd.Timestamp(year=year, month=month, day=day) if label is None else "date"


def field_selector(field_name='.*', row_id='.*', data_type='.*'):
    """
    selects a field with the argument regexp

    the following formats are accepted

    <field> [<id>] [=] <data> <data_type> <remarks>

    capture ends with: newline or EOF
    """
    if field_name != '.*':
        pre_name = f'field_{field_name}'
    elif row_id != '.*':
        pre_name = f'id_{row_id}'
    elif data_type != '.*':
        pre_name = f'type_{data_type}'
    else:
        pre_name = 'generic'

    def _field_selector(file_str, label=None):
        regexp = re.compile(
            rf"\n({field_name})\s+\[({row_id})\]\s+(=*)\s*(.*)\s+\(({data_type})\).*(\n|\Z)",
            flags=re.IGNORECASE)
        match = regexp.search(file_str)
        field_value = None if match is None else match.group(1).strip()
        return match.group(4).strip() if label is None else field_value
    _field_selector.__name__ = f'{pre_name}_field_selector'
    return _field_selector


def key_value_selector(key_name, value_regexp='.*', column_name=None):
    if column_name is None:
        column_name = key_name

    def _key_value_selector(file_str, label=None):
        regexp = re.compile(
            rf"{key_name}\s*=\s*({value_regexp})(\s*|\n)"
        )
        match = regexp.search(file_str)
        return match.group(1).strip() if label is None else column_name
    _key_value_selector.__name__ = f'{column_name}_key_value_selector'
    return _key_value_selector
