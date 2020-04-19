"""
stc.filesys
~~~~~~~

Filesystem utils
"""

import os
from stc.utils import expand_path


def get_files_from_dir(path):
    """
    Given a path to a directory, list all of its files
    """
    return os.listdir(expand_path(path))
