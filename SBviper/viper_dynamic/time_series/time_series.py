import numpy
import copy
import math


class TimeSeries:
    """
    Representation of a time series

    Attributes
    -------
    _variable : string
        the name of the specie for this TimeSeries instance
    _time_points : numpy.ndarray
        an array of time points
        time[0] = time_start
        time[len(time) - 1] = time_end
    _values : numpy.ndarray
        an array of values for the simulation corresponding to time_points
        values[0] represents the value of the specie at time[0]

    Methods
    -------
    variable()
        Get the name of the variable for this TimeSeries instance
    time_points()
        Get an array of *the current* time points for this TimeSeries
    values()
        Get an array of *the current* values for this TimeSeries
    size()
        The size of the current TimeSeries
    get_value_at_time(time_point)
        Get the value at the specified time_point
    replace_values_at_times(time_points, new_values)
        Replace the value at time points in time_points with values in new_values
    __getitem__(time_point)
    __setitem__(time_point, new_value)
    """

    def __init__(self, variable, time_points, values):
        """
        Parameters
        -------
        variable : str
            the name of the specie for this TimeSeries
        time_points : numpy.ndarray
            an array of time points for the simulation
        values : numpy.ndarray
            an array of values for the simulation corresponding to time_points
        """
        self._variable = variable
        self._time_points = copy.deepcopy(time_points)
        self._values = copy.deepcopy(values)

    @staticmethod
    def _binary_search(array, target):
        """
        Get the index of the target in the input array

        Parameters
        -------
        array : 1-D array (numpy.ndarray)
            a sorted 1-D array, the result is undefined if not sorted
        target : int
            the target value to find in the array

        Returns
        -------
        int:
            the index of the target value in the input array
            if duplicates exists, any could be returned
            if no such value exists in the array, -1 is returned
            if the input array is not sorted, the return value is undefined
        """
        left = 0
        right = len(array) - 1
        while left <= right:
            mid = int(left + (right - left) / 2)
            # value is compared with an absolute tolerance
            # TODO: confirm abs_tol
            if math.isclose(array[mid], target, abs_tol=0.00003):
                return mid
            elif array[mid] > target:
                right = mid - 1
            else:
                left = mid + 1
        return -1

    @property
    def variable(self):
        """
        Get the name of the variable for this TimeSeries instance

        Returns
        -------
        str:
            the name of the variable for this TimeSeries instance
        """
        return self._variable

    @property
    def time_points(self):
        """
        Get an array of *the current* time points for this TimeSeries

        Returns
        -------
        numpy.ndarray:
            a deep copy of the array of time points
        """
        return copy.deepcopy(self._time_points)

    @property
    def values(self):
        """
        Get an array of *the current* values for this TimeSeries

        Returns
        -------
        numpy.ndarray:
            a deep copy of the array of values for the simulation corresponding to time_points
        """
        return copy.deepcopy(self._values)

    @property
    def size(self):
        """
        Get the size of the TimeSeries

        Returns
        -------
        int:
            the size of the current time series
        """
        return self._values.shape[0]

    def get_value_at_time(self, time_point):
        """
        Get the value at the specified time_point

        Raises
        ------
        ValueError:
            if the input time_point does not exist in the simulation data

        Returns
        -------
        numpy.float64:
            the value at the specified time_point, or None if not exist
        """
        index = self._binary_search(self._time_points, time_point)
        if index == -1:
            raise ValueError("Input time_point does not exist in the simulation data")
        return self._values[index]

    def replace_values_at_times(self, time_points, new_values):
        """
        Replace the value at time points in time_points with values in new_values

        Parameters
        -------
        time_points : numpy.ndarray
            an array of time_points corresponding to the values being replaced
        new_values : numpy.ndarray
            an array of values to replace the values in the current array

        Raises
        ------
        ValueError:
            if the input time_points does not exist in the simulation data
        """
        if len(time_points) < 0 or len(new_values) < 0:
            raise ValueError("Input data cannot be empty")
        original_index = self._binary_search(self._time_points, time_points[0])
        if original_index == -1:
            raise ValueError("Input time_point does not exist in the simulation data")
        for i in range(len(time_points)):
            # value is compared with an absolute tolerance
            # TODO: confirm abs_tol
            if original_index >= len(self._time_points) or not math.isclose(self._time_points[original_index],
                                                                            time_points[i], abs_tol=0.00003):
                raise ValueError("Input time_point does not exist in the simulation data")
            self._values[original_index] = new_values[i]
            original_index += 1

    def __getitem__(self, time_point):
        return self._values[time_point]

    def __setitem__(self, time_point, new_value):
        self._values[time_point] = new_value
