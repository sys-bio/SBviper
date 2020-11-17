class TimeSeriesMatcher:
    """
    Representation of a time series matcher
    User specifies filters to use
    
    Attributes
    -------
    _tsc_original : TimeSeriesCollection
        The TimeSeriesCollection representing the original model
    _tsc_revised : TimeSeriesCollection
        The TimeSeriesCollection representing the revised model
    _filters : list of Filter

    Methods
    -------
    add_filter(function, tol)
        Add a new filter to the matcher
    """

    def __init__(self, tsc_original, tsc_revised):
        """
        Parameters
        ----------
        tsc_original : TimeSeriesCollection
            the time series collection representing the simulation result of the original model

        tsc_revised : TimeSeriesCollection
            the time series collection representing the simulation result of the revised model
        """
        self._tsc_original = tsc_original
        self._tsc_revised = tsc_revised
        self._filters = []

    def add_filter(self, filter):
        """
        Add a new filter to the matcher

        Parameters
        ----------
        filter : Filter
            a Filer object that represents a filter
        """
        self._filters.append(filter)

    def run(self):
        """
        Run the filter, iteratively, on both TimeSeriesCollection

        Raises
        ------
        ValueError:
            if an invalid function was added

        Returns
        -------
        MatchResultCollection
            containing time series data that wasn't filtered out by the filters
        """
        #TODO
        pass

