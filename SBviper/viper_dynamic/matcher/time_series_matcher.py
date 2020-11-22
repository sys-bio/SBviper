from SBviper.viper_dynamic.match_result.collection_match_result import \
    MatchResultCollection
from SBviper.viper_dynamic.match_result.match_result import MatchResult
from SBviper.viper_dynamic.Filter.filter_result import FilterResult


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
            the time series collection representing the s
            imulation result of the original model

        tsc_revised : TimeSeriesCollection
            the time series collection representing the
            simulation result of the revised model
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
        return self.__run_helper(self._filters)

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
        return self.__run_helper(list(ts_filter))

    def __run_helper(self, filters):
        filtered_collection = MatchResultCollection()
        non_filtered_collection = MatchResultCollection()
        '''
        0: iterate through the original ts collection
            0.0: add to a set of visited variables
            0.1: if the variable does not exist in the revised ts collection
                -> create MatchResult with None filter results and
                   None revised ts
                -> add to MatchResultCollection
            0.2: (variable exist in both tsc)
                0.2.0: create MatchResult
                0.2.1: iterate through filters
                    0.2.1.0: create FilterResult based on the 
                             run result of the filter
                    0.2.1.1: add FilterResult to 
                             MatchResult.FilterResultCollection
                0.2.2: add to MatchResultCollection
        1: iterate through the revised ts collection
            1.1: if the variable does not exist in the set of visited variables
                -> create MatchResult with None filter results and None original
                   ts
        '''
        visited = set()
        # iterate through the original ts collection
        for variable in self._tsc_original.variables:
            # add to a set of visited variables
            visited.add(variable)
            # if the variable does not exist in the revised ts collection
            if variable not in self._tsc_revised:
                # create MatchResult with None filter results and None
                # revised ts add to MatchResultCollection
                non_filtered_collection.add_match_result(variable,
                                                         MatchResult(
                                                             self._tsc_original[
                                                                 variable],
                                                             None))
                continue
            # variable exist in both tsc
            # create MatchResult
            match_result = MatchResult(self._tsc_original[variable],
                                       self._tsc_revised[variable])
            # iterate through filters
            filtered = False
            for filter in filters:
                # create FilterResult based on the run result of the filter
                score, tol, result = \
                    filter.run_filter(self._tsc_original[variable],
                                      self._tsc_revised[
                                          variable])
                if result:
                    filtered = True
                filter_result = FilterResult(score, tol, result)
                # add FilterResult to MatchResult.FilterResultCollection
                match_result.filter_results.add_filter_result(filter,
                                                              filter_result)
            # add to MatchResultCollection
            if filtered:
                filtered_collection.add_match_result(variable,
                                                     match_result)
            else:
                non_filtered_collection.add_match_result(variable,
                                                         match_result)
        # iterate through the revised ts collection
        for variable in self._tsc_revised.variables:
            # if the variable does not exist in the set of visited variables
            if variable not in visited:
                # create MatchResult with None filter results and None original
                # ts
                non_filtered_collection.add_match_result(variable,
                                                         MatchResult(
                                                             None,
                                                             self._tsc_revised[
                                                                 variable]))
        return filtered_collection, non_filtered_collection
