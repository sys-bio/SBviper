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
    add_time_series(species, time_series)
        Add a new TimeSeries object of a species to this TimeSeriesCollection
    get_time_series(species)
        Get the corresponding TimeSeries object of the species
    get_all_species()
        Return an array of all species in the collection
    get_all_time_series()
        Return an array of all TimeSeries objects in the collection
    get_number_of_time_series()
        Return the number of TimeSeries objects in the collection
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
    def from_nd_array(cls, simulation_result):
        """
        Create a TimeSeriesCollection object from the roadrunner's simulation result

        Parameters
        ----------
        simulation_result : numpy.ndarray
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
        Helper function for creating a dict of species name (str) to the corresponding
        TimeSeries object

        Parameters
        ----------
        simulation_result : numpy.ndarray
            the output of the simulation
        col_names : list or tuple
            the column names of the simulation result

        Raises
        ------
        ValueError:
            if the input is not a valid simulation result from roadrunner

        Returns
        -------
        dict:
            a dict from species name (str) to the corresponding TimeSeries object
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

    def add_time_series(self, species, time_series):
        """
        Add a new TimeSeries object of a species to this TimeSeriesCollection

        Parameters
        ----------
        species : str
            the name of the species to be added
        time_series : TimeSeries
            the TimeSeries object to be added to this collection

        Raises
        ------
        ValueError:
            if the input is not a valid TimeSeries object
        """
        if isinstance(time_series, TimeSeries):
            self._time_series_dict[species] = time_series
        else:
            raise ValueError("Input must be a valid TimeSeries object")

    def get_time_series(self, species):
        """
        Get the corresponding TimeSeries object of the species

        Parameters
        ----------
        species : str
            the name of the species to get

        Returns
        -------
        TimeSeries:
            the corresponding TimeSeries, None if not found
        """
        try:
            return self._time_series_dict[species]
        except KeyError:
            return None

    def get_all_species(self):
        """
        Return an array of all species in the collection

        Returns
        -------
        numpy.ndarray (str):
            all species in the collection
        """
        return numpy.array(list(self._time_series_dict.keys()))

    def get_all_time_series(self):
        """
        Return an array of all TimeSeries objects in the collection

        Returns
        -------
        numpy.ndarray:
            all TimeSeries objects in the collection
        """
        return numpy.array(list(self._time_series_dict.values()))

    def get_number_of_time_series(self):
        """
        Return the number of (species, TimeSeries) paris in the collection

        Returns
        -------
        int:
            the number of (species, TimeSeries) paris in the collection
        """
        return len(self._time_series_dict)
