"""
utils
~~~~~~~~~

Utility functions
"""

import os
import calendar

from typing import List, Optional


def list_range(start: int, stop: Optional[int] = None) -> List[int]:
    """
    Generate a list ranging from start to stop, or otherwise start length starting from 0
    """
    if stop is None:
        return list(range(start))
    return list(range(start, stop + 1))


def flatten(list_2d):
    return [item for sublist in list_2d for item in sublist]


_MONTH_DICT = {name: num for num,
               name in enumerate(calendar.month_abbr) if num}


def month_dict(month: str) -> Optional[int]:
    """
    Converts abbreviated month (3 letter month) to int value
    """
    try:
        return _MONTH_DICT[month.lower().capitalize()]
    except KeyError:
        return None


def regexp_space_between(regexp: str) -> str:
    """
    Insert optional whitespace regex between each character of regexp
    """
    return ''.join(list(sum(zip(regexp, [r'\s*' for i in range(len(regexp))]), ())))


def get_path(message: str) -> str:
    """
    Given a message, request input and run `evalPath` on it
    """
    return expand_path(input(f'{message}:\n  '))


def expand_path(path: str) -> str:
    """
    Expand environment variables and '~' in path string
    """
    return os.path.expandvars(os.path.expanduser(path))


def join_path(first_path: str, second_path: str) -> str:
    """
    Concat two path strings
    """
    return os.path.join(expand_path(first_path), expand_path(second_path))


def get_basename_from_path(file_path: str) -> str:
    """
    Extract filename from path
    """
    return os.path.basename(file_path)
