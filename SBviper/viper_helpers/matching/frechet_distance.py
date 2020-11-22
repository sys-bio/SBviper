def frechet_distance(original, revised):
    """
    Determine whether two time series is an exact match
    Assumption: len(original) = len(revised)

    Parameters
    ----------
    original: array-like
        the original time series
    revised: array-like
        the original time series

    Returns
    -------
    double:
        The Frechet distance (https://en.wikipedia.org/wiki/Fréchet_distance)
        of the two time series

    Raises
    ------
    ValueError:
        original and revised do not have the same length
    """
    if len(original) != len(revised):
        raise ValueError("The length of both time series needs to be the same!")
    score = 0
    for i in range(len(original)):
        score = max(score, abs(original[i] - revised[i]))
    return score
