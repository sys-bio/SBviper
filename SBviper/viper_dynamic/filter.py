class Filter:
    """
    Representation of a filter for the TimeSeriesMatcher
    Used for users to define filters for their model

    Attributes
    -------
    _filter_function : Function
        The function used to calculate a quantified value that
        represents the similarity of two time series in the model
        The function should take in two TimeSeries or array like
        objects, and returns a value

    _tol : double
        The tolerance value for the filter
        If the value calculated by the filter function is greater than
        the tolerance value, the time series pair will be captured by
        the filter

    Methods
    -------
    get_tol()
        Return the tolerance value for this filter object

    get_filter_function()
        Return the filter function for this filter object

    set_tol(new_tol)
        Set the tolerance value for this filter object
        Return the old tol value

    set_filter_function(new_filter_function)
        Set the filter function for this filter object
        Return the old filter function

    run_filter()
        Run the filter and return a boolean value representing whether
        the time series is captured by the filter or not
    """

    def __init__(self, filter_function, tol):
        """
        Parameters
        ----------
        filter_function : Function
            a function that takes in two TimeSeries objects, or two array
            like objects and returns a value representing the similarity
            of the two objects representing time series

        tol : double
            a tolerance value for the filter function
        """
        self._filter_function = filter_function
        self._tol = tol

    def get_tol(self):
        """
        Returns
        -------
        double
            the current tolerance value for the filter
        """
        return self._tol

    def get_filter_function(self):
        """
        Returns
        -------
        Function
            the current filter function for the filter
        """
        return self._filter_function

    def set_tol(self, new_tol):
        """
        Parameters
        ----------
        new_tol : double
            the new tolerance value for the filter

        Returns
        -------
        double
            the old tolerance value for the filter
        """
        res = self._tol
        self._tol = new_tol
        return res

    def set_filter_function(self, new_filter_function):
        """
        Parameters
        ----------
        new_filter_function : Function
            the new filter function for the filter

        Returns
        -------
        double
            the old filter function for the filter function
        """
        res = self._filter_function
        self._filter_function = new_filter_function
        return res

    def run_filter(self, ts_a, ts_b):
        """
        Parameters
        ----------
        ts_a : TimeSeries / array like
        ts_b : TimeSeries / array like

        Returns
        -------
        double
            the output of the filter function
        boolean
            true if and only if the time series is captured by
            the filter
        """
        val = self._filter_function(ts_a, ts_b)
        return val, val > self._tol
