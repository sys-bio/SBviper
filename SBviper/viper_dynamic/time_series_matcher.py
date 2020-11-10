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
    _tols : list of tolerance values
        Contains the tolerance values for the filters specified by the user
        _tols[i] represents the tolerance value for the output of the filtering function _filters[i]

    Methods
    -------
    set_exact_match(tol)
        Sets exact match to be included in the filtering process, with the specified tolerance
        Tolerance is defined to be the maximum Fréchet distance
    """

    def __init__(self, tsc_original, tsc_revised):
        self._tsc_original = tsc_original
        self._tsc_revised = tsc_revised
        # Set default filer
        self._exact_match = False
        self._filters = []
        self._tols = []

    def set_filter(self, function, tol):
        self._filters.append(function)
        self._tols.append(tol)
