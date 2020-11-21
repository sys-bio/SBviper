class FilterResultCollection:
    """
    Representation of a collection of filter results from the matcher

    Attributes
    ----------
    _filter_result_dict : dict

    Methods
    -------
    filters() : numpy.ndarray
        Return an array of instances to filters that generated the filter results
    filter_results() : numpy.ndarray
        Return an array of filter results associated with this collection
    size() : int
        The size of the collection
    add_filter_result(filter, filter_result) : void
        Add a new FilterResult object of a filter to this collection
    get_filter_result(filter) : FilterResult
        Get the corresponding FilterResult object of the variable
    __getitem__(filter)
    __setitem__(filter, filter_result)
    __len__()
    __contains__(filter)
    """

    def __init__(self):
        self._filter_result_dict = {}