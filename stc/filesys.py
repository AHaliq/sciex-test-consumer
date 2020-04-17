"""
stc.filesys
~~~~~~~

Filesystem utils
"""

import os


def get_files_from_dir(path):
    return [x for x in os.listdir(path)]
