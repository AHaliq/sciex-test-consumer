"""
filesys
~~~~~~~

Filesystem utils
"""

import os
import pkgutil
import importlib

from utils import expand_path


def get_files_from_dir(path):
    """
    Given a path to a directory, list all of its files
    """
    return os.listdir(expand_path(path))


def get_modules_in_pkg(pkg):
    pkgpath = os.path.dirname(pkg.__file__)
    return [name for _, name, _ in pkgutil.iter_modules([pkgpath])]


def dynamic_import(pkgname):
    return importlib.import_module(pkgname)
