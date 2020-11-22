"""Commonly used utilities."""

import os
from SBviper.viper_dynamic.time_series.collection_time_series import \
    TimeSeriesCollection


def get_abs_path(filename):
    """
    gets the absolute path to the file

    Parameters
    ----------
    filename: str
        the filename to be parsed

    Returns
    -------
    str:
        absolute path
    """
    dirname = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(dirname, filename)


def get_tsc_from_SBML(original_path, revised_path):
    pass


def get_tsc_from_CSV(original_path, revised_path):
    """
    get tsc from csv file

    Parameters
    ----------
    original_path: str
        path to the original csv file
    revised_path: str
        path to the revised csv file

    Raises
    ------
    ValueError:
        invalid path

    Returns
    -------
    TimeSeriesCollection:
        original tsc
    TimeSeriesCollection:
        revised tsc
    """
    if not os.path.isfile(original_path) or not os.path.isfile(revised_path):
        original_path = get_abs_path(original_path)
        revised_path = get_abs_path(revised_path)
        if not os.path.isfile(original_path) or not os.path.isfile(
                revised_path):
            raise ValueError
    original_tsc = TimeSeriesCollection.from_csv(original_path)
    revised_tsc = TimeSeriesCollection.from_csv(revised_path)
    return original_tsc, revised_tsc
