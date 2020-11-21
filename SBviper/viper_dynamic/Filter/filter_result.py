class FilterResult:
    """
    Representation of a filter result from time series matcher

    Attributes
    ----------
    _score : double
    _tol : double
    _filtered_or_not() : boolean

    Methods
    -------
    score()
        Get the score of this filter result
    tol()
        Get the tolerance of this filter result
    filtered_or_not()
        Get whether this ts pair has been filtered or not, from this filter
    """

    def __init__(self, score, tol, filtered_or_not):
        """
        Parameters
        ----------
        score : double
            the score for this filter result
        tol : double
            the tolerance for this filter result
        filtered_or_not : boolean
        """
        self._score = score
        self._tol = tol
        self._filtered_or_not = filtered_or_not

    @property
    def score(self):
        """
        Get the score of this FilterResult instance

        Returns
        -------
        double:
            score of this filter result
        """
        return self._score

    @property
    def tol(self):
        """
        Get the tolerance of this FilterResult instance

        Returns
        -------
        double:
            tol score of this filter result
        """
        return self._tol

    @property
    def filtered_or_not(self):
        """
        Get whether the ts pair has been filtered or not, from this filter

        Returns
        -------
        boolean:
            true for filtered, false for not filtered
        """
        return self._filtered_or_not

