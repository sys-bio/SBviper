import numpy as np

from SBviper.viper_dynamic.match_result.match_result import MatchResult


class MatchResultCollection:
    """
    Representation of a collection of match results from time series matcher

    Attributes
    -------
    _match_result_dict : dict
        dictionary of variable_str to the corresponding MatchResult object

    Methods
    -------
    variables()
        Return an array of all variables in the collection
    match_results()
        Return an array of all MatchResult objects in the collection
    size()
        Return the number of (variable, MatchResult) pairs in the collection
    add_match_result(variable, match_result)
        Add a new MatchResult object of a variable to this MatchResultCollection
    get_match_result(variable)
        Get the corresponding MatchResult object of the variable
    __len__()
        Return the number of MatchResult objects in this collection
    __setitem__(variable, march_result)
    __getitem__(variable)
    __contains__(variable)
    """

    def __init__(self):
        self._match_result_dict = {}

    @property
    def variables(self):
        """
        Return an array of all variables in the collection

        Returns
        -------
        numpy.ndarray(str):
            all variables in the collection
        """
        return np.array(list(self._match_result_dict.keys()))

    @property
    def match_results(self):
        """
        Return an array of all MatchResult objects in the collection

        Returns
        -------
        numpy.ndarray:
            all MatchResult in the collection
        """
        return np.array(list(self._match_result_dict.values()))

    @property
    def size(self):
        """
        Return the number of (variable, MatchResult) pairs in the collection

        Returns
        -------
        int:
            the number of (variable, MatchResult) paris in the collection
        """
        return len(self._match_result_dict)

    def add_match_result(self, variable, match_result):
        """
        Add a new MatchResult object of a variable to this MatchResultCollection

        Parameters
        ------
        variable : str
            the name of the variable to be added
        match_result : MatchResult
            the MatchResult object to be added to this collection

        Raises
        ------
        ValueError:
            if the input is not a valid TimeSeries object
        """
        if isinstance(match_result, MatchResult):
            self._match_result_dict[variable] = match_result
        else:
            raise ValueError("Input must be a valid TimeSeries object")

    def get_match_result(self, variable):
        """
        Get the corresponding MatchResult object of the variable

        Parameters
        ------
        variable : str
            the name of the variable to get

        Returns
        -------
        MatchResult:
            the corresponding MatchResult, None if not found
        """
        try:
            return self._match_result_dict[variable]
        except KeyError:
            return None

    def __len__(self):
        return self.size

    def __setitem__(self, variable, march_result):
        self.add_match_result(variable, march_result)

    def __getitem__(self, variable):
        return self.get_match_result(variable)

    def __contains__(self, variable):
        return variable in self._match_result_dict