import numpy as np
from SBviper.viper_dynamic.Filter.filter import Filter
from SBviper.viper_dynamic.Filter.filter_result import FilterResult


class FilterResultCollection:
    """
    Representation of a collection of filter results from the matcher

    Attributes
    ----------
    _filter_result_dict : dict

    Methods
    -------
    filters() : numpy.ndarray
        Return an array of instances to filters that generated the
        filter results
    filter_results() : numpy.ndarray
        Return an array of filter results associated with this collection
    size() : int
        The size of the collection
    add_filter_result(filter, filter_result) : void
        Add a new FilterResult object of a filter to this collection
    get_filter_result(filter) : FilterResult
        Get the corresponding FilterResult object of the variable
    __len__()
    __getitem__(filter)
    __setitem__(filter, filter_result)
    __contains__(filter)
    """

    def __init__(self):
        self._filter_result_dict = {}

    @property
    def filters(self):
        """
        Return an array of all filters in the collection

        Returns
        -------
        numpy.ndarray(Filter)
            all filters in the collection
        """
        return np.array(list(self._filter_result_dict.keys()))

    @property
    def filter_results(self):
        """
        Return an array of all filter results in the collection

        Returns
        -------
        numpy.ndarray(FilterResult)
            all filter results in the collection
        """
        return np.array(list(self._filter_result_dict.values()))

    @property
    def size(self):
        """
        Return the number of (Filter, FilterResult) pairs in the collection

        Returns
        -------
        int:
            the number of (Filter, FilterResult) pairs in the collection
        """
        return len(self._filter_result_dict)

    def add_filter_result(self, filter, filter_result):
        """
        Add a new FilterResult object of a filter to this collection

        Parameters
        ----------
        filter : Filter
            the filter instance
        filter_result : FilterResult
            the filter result instance

        Raises
        ------
        ValueError:
        if the input is not a valid Filter/FilterResult object
        """
        if isinstance(filter, Filter) and \
                isinstance(filter_result, FilterResult):
            self._filter_result_dict[filter] = filter_result
        else:
            raise ValueError("invalid input")

    def get_filter_result(self, filter):
        """
        Get the corresponding FilterResult object of the filter

        Parameters
        ----------
        filter : Filter
            the filter

        Returns
        -------
        FilterResult:
            the corresponding FilterResult, None if not found
        """
        try:
            return self._filter_result_dict[filter]
        except KeyError:
            return None

    def __len__(self):
        return self.size

    def __setitem__(self, variable, march_result):
        self.add_filter_result(variable, march_result)

    def __getitem__(self, variable):
        return self.get_filter_result(variable)

    def __contains__(self, variable):
        return variable in self._filter_result_dict
