import numpy as np
import math
from SBviper.viper_dynamic.time_series import TimeSeries
import matplotlib.pyplot as plt

class DerivativeDTW:
    """
    A implementation of the Derivative Dynamic Time Warping algorithm for comparing the similarity,
    and calculate the distance between two time series
    https://www.ics.uci.edu/~pazzani/Publications/sdm01.pdf
    https://github.com/KishoreKaushal/DerivativeDynamicTimeWarping/blob/master/.ipynb_checkpoints/Time_Series_
    Clustering-checkpoint.ipynb

    Attributes
    -------
    _time_series_a : TimeSeries
        a TimeSeries representation of the time series
    _time_series_b : TimeSeries
        a TimeSeries representation of the time series

    Methods
    -------
    compute()
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
        self.__compute_derivative_matrix()

    def __compute_derivative_matrix(self):
        """
        Compute the derivative matrix for estimating the dtw value
        """
        self._derivative_matrix_a = self.__get_derivative_matrix(self._time_series_a)
        self._derivative_matrix_b = self.__get_derivative_matrix(self._time_series_b)
        print(self._derivative_matrix_a)
        print(self._derivative_matrix_b)

    @staticmethod
    def __get_derivative_matrix(ts):
        """
        Estimate the derivative matrix
        """
        derivative_matrix = np.zeros(ts.size)
        for i in range(1, ts.size - 1):
            derivative_matrix[i] = ((ts[i] - ts[i - 1]) + ((ts[i + 1] - ts[i - 1]) / 2)) / 2
        derivative_matrix[0] = derivative_matrix[1]
        derivative_matrix[-1] = derivative_matrix[-2]
        return derivative_matrix

    def compute(self):
        """
        Computes the numerical representation of the similarity of the two time series

        Returns
        -------
        double:
            a numerical measure of the similarity between the two time series of the object
        """
        # Initialize dtw matrix
        n, m = self._time_series_a.size, self._time_series_b.size
        dtw_matrix = np.zeros((n + 1, m + 1))
        for i in range(n):
            for j in range(m):
                dtw_matrix[i + 1, j + 1] = abs(self._derivative_matrix_a[i] - self._derivative_matrix_b[j]) + \
                                           min(dtw_matrix[i, j], dtw_matrix[i, j + 1], dtw_matrix[i + 1, j])
        print(dtw_matrix)
        return dtw_matrix[n, m]

    def plot_derivative(self):
        plt.plot(self._derivative_matrix_a)
        plt.plot(self._derivative_matrix_b)
        plt.show()
