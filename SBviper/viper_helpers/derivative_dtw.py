import numpy
import math
from SBviper.viper_dynamic.time_series import TimeSeries

class DerivativeDTW:
    """
    A implementation of the Derivative Dynamic Time Warping algorithm for comparing the similarity,
    and calculate the distance between two time series
    https://www.ics.uci.edu/~pazzani/Publications/sdm01.pdf

    Attributes
    -------
    _time_series_a : TimeSeries
        a TimeSeries representation of the time series
    _time_series_b : TimeSeries
        a TimeSeries representation of the time series

    Methods
    -------
    compute_score()
        Computes the DDTW score for the two time series
    """

    def __init__(self, time_series_a, time_series_b):
        """
        Parameters
        -------
        time_series_a : TimeSeries
            a representation of one of the time series
        time_series_b : TimeSeries
            a representation of the other time series
        """
        # TODO: Input validation
        self._time_series_a = time_series_a
        self._time_series_b = time_series_b

    def compute_score(self):
        """
        Computes the numerical representation of the similarity of the two time series

        Returns
        -------
        double:
            a numerical measure of the similarity between the two time series of the object
        """
