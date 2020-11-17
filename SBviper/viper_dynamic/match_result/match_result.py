class MatchResult:
    """
    Representation of a match result from time series matcher

    Attributes
    -------
    _original_ts : TimeSeries
        the original time series
    _revised_ts : TimeSeries
        the revised time series

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
