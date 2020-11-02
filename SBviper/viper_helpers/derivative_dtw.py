import numpy
import math

def dtw(a, b):
    """
    A implementation of the Derivative Dynamic Time Warping algorithm for comparing the similarity,
    and calculate the distance between two time series
    https://www.ics.uci.edu/~pazzani/Publications/sdm01.pdf

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

