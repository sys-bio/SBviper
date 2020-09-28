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
        Create a TimeSeriesCollection object from the roadrunner's simulation result

        Parameters
        ----------
        simulation_result : NamedArray
            the output from simulating the model in roadrunner

        Raises
        ------
        ValueError:
            if the input is not a valid simulation result from roadrunner
        """
        time_series_dict = cls._create_dict_from_array(simulation_result, simulation_result.colnames)
        return cls(time_series_dict)

    @classmethod
    def from_csv(cls, path):
        """
        Create a TImeSeriesCollection object from csv file

        Parameters
        ----------
        path: str
            the path to the csv file in the current working directory

        Raises
        ------
        FileNotFoundError:
            if the csv file is not found
        ValueError:
            if the input is not a valid simulation result from roadrunner
        """
        try:
            simulation_result = numpy.genfromtxt(path, delimiter=',', names=True)
        except OSError:
            raise FileNotFoundError("File not found, check the path to the CSV file")
        time_series_dict = cls._create_dict_from_array(simulation_result, simulation_result.dtype.names)
        return cls(time_series_dict)

    @classmethod
    def from_bio_model(cls, model):
        """
        Create a TimeSeriesCollection object from a model in the BioModels repository

        Parameters
        ----------
        model : str
            the BioModel ID

        Raises
        ------
        """
        pass

    @staticmethod
    def _create_dict_from_array(simulation_result, col_names):
        """
        Parameters
        ----------
        simulation_result : numpy.ndarray
            the output of the simulation
        col_names: list or tuple
            the column names of the simulation result

        Raises
        ------
        ValueError:
            if the input is not a valid simulation result from roadrunner
        """
        time_series_dict = {}
        for col in col_names:
            if col == "time":
                continue
            col_name = col.strip("[]")
            try:
                time_series_dict[col_name] = \
                    TimeSeries(col_name, simulation_result["time"], simulation_result[col])
            # input simulation result must match expected format
            except IndexError:
                raise ValueError("Input must be the simulation result from roadrunner")
        return time_series_dict
