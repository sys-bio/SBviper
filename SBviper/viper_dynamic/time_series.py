import numpy
import copy


class TimeSeries:
    """
    Representation of a time series

    Attributes
    ----------
    _variables : string
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
    get_variables()
        Get the name of the variables for this TimeSeries instance
    get_time_points()
        Get an array of *the current* time points for this TimeSeries
    get_values()
        Get an array of *the current* values for this TimeSeries
    get_value_at_time(time_point)
        Get the value at the specified time_point
    replace_values_at(time_points, new_values)
        Replace the value at time points in time_points with values in new_values
    """

    def __init__(self, variables, time_points, values):
        """
        Parameters
        ----------
        variables : str
            the name of the specie for this TimeSeries
        time_points : numpy.ndarray
            an array of time points for the simulation
        values : numpy.ndarray
            an array of values for the simulation corresponding to time_points
        """
        self._variables = variables
        self._time_points = copy.deepcopy(time_points)
        self._values = copy.deepcopy(values)

    def get_variables(self):
        """
        Get the name of the variables for this TimeSeries instance

        Returns
        -------
        str:
            the name of the specie for this TimeSeries instance
        """
        return self._variables

    def get_time_points(self):
        """
        Get an array of *the current* time points for this TimeSeries

        Returns
        -------
        numpy.ndarray:
            a deep copy of the array of time points
        """
        return copy.deepcopy(self._time_points)

    def get_values(self):
        """
        Get an array of *the current* values for this TimeSeries

        Returns
        -------
        numpy.ndarray:
            a deep copy of the array of values for the simulation corresponding to time_points
        """
        return copy.deepcopy(self._values)

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
        pass

    def replace_values_at(self, time_points, new_values):
        """
        Replace the value at time points in time_points with values in new_values

        Parameters
        ----------
        time_points : numpy.ndarray
            an array of time_points corresponding to the values being replaced
        new_values : numpy.ndarray
            an array of values to replace the values in the current array

        Raises
        ------
        ValueError:
            if the input time_points does not exist in the simulation data
        """
        pass
