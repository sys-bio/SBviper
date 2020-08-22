"""Commonly used utilities."""

import os


def get_abs_path(filename):
    """
    gets the absolute path to the file
    :param: filename: the filename to be parsed
    :return: an absolute path
    """
    dirname = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(dirname, filename)
