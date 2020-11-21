import numpy as np

from viper_dynamic.time_series.time_series import TimeSeries


class TimeSeriesCollection:
    """
    Representation of a collection of time series

    Attributes
    ----------
    _time_series_dict : dict
        dictionary of variables_str to the corresponding TimeSeries object

    Methods
    -------
    variables()
        Return an array of all variables in the collection
    time_series()
        Return an array of all TimeSeries objects in the collection
    size()
        Return the size of the collection
    add_time_series(variable, time_series)
        Add a new TimeSeries object of a variable to this TimeSeriesCollection
    get_time_series(variable)
        Get the corresponding TimeSeries object of the variable
    __getitem__(variable)
    __setitem__(variable, time_series)
    __len__()
    __contains__(variable)
    """

    def __init__(self, time_series_dict):
        """
        Parameters
        ----------
        time_series_dict : dict
            dictionary of variables_str to the corresponding TimeSeries object
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
            simulation_result = np.genfromtxt(path, delimiter=',', names=True)
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
        Helper function for creating a dict of variables name (str) to the corresponding
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
            a dict from variables name (str) to the corresponding TimeSeries object
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

    @property
    def variables(self):
        """
        Return an array of all variables in the collection

        Returns
        -------
        numpy.ndarray(str):
            all variables in the collection
        """
        return np.array(list(self._time_series_dict.keys()))

    @property
    def time_series(self):
        """
        Return an array of all TimeSeries objects in the collection

        Returns
        -------
        numpy.ndarray:
            all TimeSeries objects in the collection
        """
        return np.array(list(self._time_series_dict.values()))

    @property
    def size(self):
        """
        Return the number of (variable, TimeSeries) paris in the collection

        Returns
        -------
        int:
            the number of (variable, TimeSeries) paris in the collection
        """
        return len(self._time_series_dict)

    def add_time_series(self, variable, time_series):
        """
        Add a new TimeSeries object of a variable to this TimeSeriesCollection

        Parameters
        ------
        variable : str
            the name of the variable to be added
        time_series : TimeSeries
            the TimeSeries object to be added to this collection

        Raises
        ------
        ValueError:
            if the input is not a valid TimeSeries object
        """
        if isinstance(time_series, TimeSeries):
            self._time_series_dict[variable] = time_series
        else:
            raise ValueError("Input must be a valid TimeSeries object")

    def get_time_series(self, variable):
        """
        Get the corresponding TimeSeries object of the variable

        Parameters
        ------
        variable : str
            the name of the variable to get

        Returns
        -------
        TimeSeries:
            the corresponding TimeSeries, None if not found
        """
        try:
            return self._time_series_dict[variable]
        except KeyError:
            return None

    def __getitem__(self, variable):
        return self.get_time_series(variable)

    def __setitem__(self, variable, time_series):
        self.add_time_series(variable, time_series)

    def __len__(self):
        return self.size

    def __contains__(self, variable):
        return variable in self._time_series_dict
