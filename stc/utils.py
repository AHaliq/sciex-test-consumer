"""
stc.utils
~~~~~~~~~

Utility functions
"""

import os
import calendar


def lr(start, stop=None):
    if stop is None:
        return list(range(start))
    else:
        return list(range(start, stop + 1))


MNTH_DICT = {name: num for num, name in enumerate(calendar.month_abbr) if num}


def regex_space_between(text):
    return ''.join(list(sum(zip(text, ['\s*' for i in range(len(text))]), ())))


def getPath(message):
    return evalPath(input(f'{message}:\n  '))


def evalPath(path):
    return os.path.expanduser(path)
