from SBviper.viper_dynamic.match_result.collection_match_result import MatchResultCollection


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
    add_filter(ts_filter)
        Add a new filter object to the matcher
    run()
        Run all of the filters
    run_filter(ts_filter)
        Run a specific filter
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

    def add_filter(self, ts_filter):
        """
        Add a new filter to the matcher

        Parameters
        ----------
        ts_filter : Filter
            a Filer object that represents a filter
        """
        self._filters.append(ts_filter)

    def run(self):
        """
        Run all of the filters, iteratively, on both TimeSeriesCollection

        Raises
        ------
        ValueError:
            if an invalid function was added

        Returns
        -------
        MatchResultCollection
            containing time series data that wasn't filtered out by the filters
        MatchResultCollection
            containing time series data that was filtered out by the filters
        """
        filtered = MatchResultCollection()
        non_filtered = MatchResultCollection()
        '''
        0: iterate through the original ts collection
            0.0: add to a set of visited variables
            0.1: if the variable does not exist in the revised ts collection
                -> create MatchResult with None filter results
            0.2: (variable exist in both tsc)
                0.2.0: create MatchResult
                0.2.0: iterate through filters
                    0.2.0.0: 
                    0.2.0.1: 
        '''

    def run_filter(self, ts_filter):
        """
        Run a specific filter on both TimeSeriesCollection

        Raises
        ------
        ValueError:
            if an invalid function was added

        Returns
        -------
        MatchResultCollection
            containing time series data that wasn't filtered out by the filters
        MatchResultCollection
            containing time series data that was filtered out by the filters
        """
        # TODO: implement run_filter
        pass
