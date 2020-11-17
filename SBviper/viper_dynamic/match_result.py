class MatchResult:
    """
    Representation of a match result from time series matcher

    Attributes
    -------
    _original_ts : TimeSeries
        the original time series
    _revised_ts : TimeSeries
        the revised time series

    # TODO: how should value be defined?
    # 1: dict that stores filter-value pairs
    #    filter needs to be run every time even if the ts pair has already been
    #    filtered out
    # 2: double that stores the value of the filter output that filters
    #    out this ts pair
    #    would this be helpful?


    Methods
    -------
    get_original_ts()
        Get the time series from the original model in this matching pair
    get_revised_ts()
        Get the time series from the revised model in this matching pair
    """

    def __init__(self, original_ts, revised_ts):
        """
        Parameters
        -------
        original_ts : TimeSeries
            the time series in the original model in this matching pair
            None if the paired time series does not exist in the original model
        revised_ts : TimeSeries
            the time series in the revised model in this matching pair
            None if the paired time series does not exist in the revised model
        """
        self._original_ts = original_ts
        self._revised_ts = revised_ts

    def get_original_ts(self):
        """
        Get the time series from the original model in this matching pair

        Returns
        -------
        TimeSeries:
            The TimeSeries object that represents the time series from the original
            model
        """
        return self._original_ts

    def get_revised_ts(self):
        """
        Get the time series from the revised model in this matching pair

        Returns
        -------
        TimeSeries:
            The TimeSeries object that represents the time series from the revised
            model
        """
        return self._revised_ts
