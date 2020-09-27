class TimeSeries:
    """
    Representation of a time series

    Attributes
    ----------
    specie : string
        the name of the specie for this TimeSeries instance
    time_points : list
        a list of time points
        time[0] = time_start
        time[len(time) - 1] = time_end
    values : list
        a list of values for the simulation corresponding to time_points
        values[0] represents the value of the specie at time[0]
    steady_states : list
        a list of SteadyState objects for this TimeSeries

    Methods
    -------
    get_specie()
        gets the name of the specie for this TimeSeries instance
    get_time_points()
        gets a list of time points for this TimeSeries
    get_values()
        gets a list of values for this TimeSeries
    get_value_at_time(time_point)
        gets the value at the specified time_point
    replace_values_at(time_points, new_values)
        replaces the value at time points in time_points with values in new_values
    """

    def __init__(self, specie, time_points, values):
        """
        Parameters
        ----------
        specie: str
            the name of the specie for this TimeSeries
        time_points: numpy.ndarray
            a list of time points for the simulation
        values: numpy.ndarray
            a list of values for the simulation corresponding to time_points
        """
