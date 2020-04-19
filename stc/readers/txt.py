"""
readers.txt
~~~~~~~~~~~~~~~

Read txt files util
"""

from utils import expand_path


def txt_file_to_str(path):
    """
    Given a path to a textfile, read its contents
    """
    return open(expand_path(path)).read()
