import numpy
import math

def dtw(a, b):
    """
    A implementation of the Dynamic Time Warping algorithm for comparing the similarity, and calculate the distance
    between two time series

    Parameters
    -------
    a : TimeSeries
        a TimeSeries representation of the time series
    b : TimeSeries
        a TimeSeries representation of the time series

    Raises
    -------
    ValueError:


    Returns
    -------
    float:
        a numerical representation of the distance between the two time series
    """
