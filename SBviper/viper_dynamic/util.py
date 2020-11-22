"""Commonly used utilities."""

import os
from SBviper.viper_dynamic.time_series.collection_time_series import \
    TimeSeriesCollection
import tellurium as te


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


def get_tsc_from_Ant(original_path, revised_path):
    """
    get tsc from Antimony file

    Parameters
    ----------
    original_path: str
        path to the original Antimony file
    revised_path: str
        path to the revised Antimony file

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
    original_model = te.loada(original_path)
    revised_model = te.loada(revised_path)
    # TODO: Making an assumption here
    original_result = original_model.simulate(0, 100, 1000)
    revised_result = revised_model.simulate(0, 100, 1000)
    original_tsc = TimeSeriesCollection.from_nd_array(original_result)
    revised_tsc = TimeSeriesCollection.from_nd_array(revised_result)
    return original_tsc, revised_tsc


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

def get_tsc_from_SBML(original_path, revised_path):
    """
    get tsc from SBML file

    Parameters
    ----------
    original_path: str
        path to the original SBML file
    revised_path: str
        path to the revised SBML file

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
    original_model = te.loadSBMLModel(original_path)
    revised_model = te.loadSBMLModel(revised_path)
    # TODO: Making an assumption here
    original_result = original_model.simulate(0, 100, 1000)
    revised_result = revised_model.simulate(0, 100, 1000)
    original_tsc = TimeSeriesCollection.from_nd_array(original_result)
    revised_tsc = TimeSeriesCollection.from_nd_array(revised_result)
    return original_tsc, revised_tsc
