class SteadyState:
    """
    Representation of a steady state for a time series

    Attributes
    ----------
    time_point : int  # TODO: should this be list instead?
    value: int

    Methods
    -------
    get_time()
        gets the time point where the steady state occurred
    get_value()
        gets the value where the steady state occurred
    equal(target, time_tol=TTOL, value_tol=VTOL)
        checks if both steady states are reached at the equivalent
        value and time point within the tolerance range
    compare_to_time(target, low, high)
        checks if this steady state is reached at time that is [low, high]
        time points later than the target steady state
    compare_to_time(target, time_tol=TTOL)
        checks if both steady states are reached at the equivalent
        time point within the tolerance range
    compare_to_value(target, low, high)
        checks if this steady state is reached at a value that is [low, high]
        times greater than the target steady state
    compare_to_value(target, value_tol=VTOL)
        checks if both steady states are reached at the equivalent
        value within the tolerance range
    """