"""
stc.utils
~~~~~~~~~

Utility functions
"""


def lr(start, stop=None):
    if stop is None:
        return list(range(start))
    else:
        return list(range(start, stop + 1))
