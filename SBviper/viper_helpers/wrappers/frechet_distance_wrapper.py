from SBviper.viper_helpers.matching.frechet_distance import frechet_distance

def frechet_distance_wrapper(original, revised):
    """
    Wrapper function for frechet_distance
    NOTE: tolerance should be hard coded in this function

    Parameters
    ----------
    original: TimeSeries
        the original time series
    revised: TimeSeries
        the original time series

    Returns
    -------
    double:
        quantified value for the similarity
    double:
        tolerance used for this match
    boolean:
        indication of whether the ts pair has been filtered or not
    """
    score = frechet_distance(original, revised)
    return score, 5.0, score >= 5.0
