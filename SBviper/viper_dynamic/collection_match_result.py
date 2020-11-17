class MatchResultCollection:
    """
    Representation of a collection of match results from time series matcher

    Attributes
    -------
    _match_result_dict : dict
        dictionary of variables_str to the corresponding MatchResult object

    Methods
    -------
    add_match_result(variable, match_result)
        Add a new MatchResult object of a variable to this MatchResultCollection
    get_match_result(variable)
        Get the corresponding MatchResult object of the variable
    variables()
        Return an array of all variables in the collection
    match_result()
        Return an array of all MatchResult objects in the collection
    __len__()
        Return the number of MatchResult objects in this collection
    """