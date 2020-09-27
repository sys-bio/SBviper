import numpy

from SBviper.viper_dynamic.time_series import TimeSeries


class TimeSeriesCollection:
    """
    Representation of a collection of time series

    Attributes
    ----------
    _time_series_dict : dict
        dictionary of species_str to the corresponding TimeSeries object

    Methods
    -------
    add_time_series(species, ts)
        adds a new TimeSeries of a species to the collection
    get_time_series(species)
        gets the corresponding TimeSeries object of the species
    get_all_time_series()
        returns a list of all of the TimeSeries objects in the collection
    get_number_of_time_series()
        returns the number of TimeSeries objects in the collection
    """

    def __init__(self, time_series_dict):
        """
        Parameters
        ----------
        time_series_dict : dict
            dictionary of species_str to the corresponding TimeSeries object
        """
        self._time_series_dict = time_series_dict

    @classmethod
    def from_named_array(cls, simulation_result):
        """
        Parameters
        ----------
        simulation_result : NamedArray
            the output from simulating the model in roadrunner

        Raises
        ------
        RuntimeError:
            if the input is not a valid simulation result from roadrunner
        """
        time_series_dict = {}
        for col in simulation_result.colnames:
            if col == "time":
                continue
            col_name = col.strip("[]")
            try:
                time_series_dict[col_name] = \
                    TimeSeries(col_name, simulation_result["time"], simulation_result[col])
            # input simulation result must match expected format
            except IndexError:
                raise RuntimeError("Input must be the simulation result from roadrunner, try CSV file input instead")
        return cls(time_series_dict)

    @classmethod
    def from_csv(cls, path):

