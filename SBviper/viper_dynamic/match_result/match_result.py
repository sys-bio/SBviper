from SBviper.viper_dynamic.Filter.collection_filter_result import FilterResultCollection


class MatchResult:
    """
    Representation of a match result from time series matcher

    Attributes
    ----------
    _original_ts : TimeSeries
        the original time series
    _revised_ts : TimeSeries
        the revised time series
    _filter_results : FilterResultCollection

    Methods
    -------
    original_ts()
        Get the time series from the original model in this matching pair
    revised_ts()
        Get the time series from the revised model in this matching pair
    """

    def __init__(self, original_ts, revised_ts):
        """
        Parameters
        ----------
        original_ts : TimeSeries
            the time series in the original model in this matching pair
            None if the paired time series does not exist in the original model
        revised_ts : TimeSeries
            the time series in the revised model in this matching pair
            None if the paired time series does not exist in the revised model
        """
        self._original_ts = original_ts
        self._revised_ts = revised_ts
        self._filter_results = FilterResultCollection()

    @property
    def original_ts(self):
        """
        Get the time series from the original model in this matching pair

        Returns
        -------
        TimeSeries:
            The TimeSeries object that represents the time series from the original
            model
        """
        return self._original_ts

    @property
    def revised_ts(self):
        """
        Get the time series from the revised model in this matching pair

        Returns
        -------
        TimeSeries:
            The TimeSeries object that represents the time series from the revised
            model
        """
        return self._revised_ts

    @property
    def filter_results(self):
        """
        Get the filter result for this pair of match

        Returns
        -------
        FilterResultCollection
        """
        return self._filter_results
