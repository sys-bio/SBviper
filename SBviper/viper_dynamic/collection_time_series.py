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