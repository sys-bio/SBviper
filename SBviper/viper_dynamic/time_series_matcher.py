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
    _filters : list of functions
        Contains a list of functions for the filter
    _tol_vals : list of tolerance values
        Contains the tolerance values for the filters specified by the user
        _tol_vals[i] represents the tolerance value for the output of the filtering function _filters[i]

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
        # Set default filer
        self._exact_match = False
        self._filters = []
        self._tol_vals = []

    def add_filter(self, function, tol):
        """
        Add a new filter to the matcher

        Parameters
        ----------
        function: a python function(original_ts, revised_ts)
            the function should take in two arguments, either in the form of numpy.ndarray or TimeSeries,
            the first argument represents time-value pairs in the original simulation, while the second
            argument represents time-value pairs in the revised simulation. The function should output
            a quantified numerical value that represents the similarity, to some extend, of the time-value
            pairs, which is then compared with the tolerance value.
        tol : double
            a numerical value that represents the tolerance value of the filter function
        """
        self._filters.append(function)
        self._tol_vals.append(tol)

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
        for i in range(len(self._filters)):

