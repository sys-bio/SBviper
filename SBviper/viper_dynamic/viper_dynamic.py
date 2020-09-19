class TimeSeriesCollection:
    """
    Representation of a collection of time series

    Attributes
    ----------
    time_series_dict : dict
        dictionary of species_str to the corresponding TimeSeries object

    Methods
    -------
    add_time_series(species, ts)
        adds a new TimeSeries of a species to the collection
    get_time_series(species)
        gets the corresponding TimeSeries object of the species
    get_all_time_series()
        returns a list of all of the TimeSeries objects in the collection
    get_number_of_time_series()
        returns the number of TimeSeries objects in the collection
    """

    def __init__(self, simulation_result):
        """
        Parameters
        ----------
        simulation_result : NamedArray
        """
        self.time_series_dict = {}


class TimeSeries:
    """
    Representation of a time series

    Attributes
    ----------
    species : string
        the name of the species for this TimeSeries instance
    time_points : list
        a list of time points
        time[0] = time_start
        time[len(time) - 1] = time_end
    values : list
        a list of values corresponding to the list of time
        values[0] represents the value of the species at time[0]
    steady_states : list
        a list of SteadyState objects for this TimeSeries

    Methods
    -------
    get_species()
        gets the name of the species for this TimeSeries instance
    get_time_points()
        gets a list of time points for this TimeSeries
    get_values()
        gets a list of values for this TimeSeries
    get_value_at_time(time_point)
        gets the value at the specified time_point
    replace_values_at(time_points, new_values)
        replaces the value at time points in time_points with values in new_values
    """

    def __init__(self, species, time_points, values):
        self.species = species
        self.time_points = time_points
        self.values = values


class SteadyState:
    """
    Representation of a steady state for a time series

    Attributes
    ----------
    time_point : int  # TODO: should this be list instead?
    value: int

    Methods
    -------
    get_time()
        gets the time point where the steady state occurred
    get_value()
        gets the value where the steady state occurred
    equal(target, time_tol=TTOL, value_tol=VTOL)
        checks if both steady states are reached at the equivalent
        value and time point within the tolerance range
    compare_to_time(target, low, high)
        checks if this steady state is reached at time that is [low, high]
        time points later than the target steady state
    compare_to_time(target, time_tol=TTOL)
        checks if both steady states are reached at the equivalent
        time point within the tolerance range
    compare_to_value(target, low, high)
        checks if this steady state is reached at a value that is [low, high]
        times greater than the target steady state
    compare_to_value(target, value_tol=VTOL)
        checks if both steady states are reached at the equivalent
        value within the tolerance range
    """
