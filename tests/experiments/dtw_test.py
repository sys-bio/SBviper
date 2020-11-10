import numpy as np
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
import tellurium as te # Python-based modeling environment for kinetic models
import tkinter
import roadrunner as rr # High-performance simulation and analysis library
import numpy as np # Scientific computing package
import random # Generate random numbers
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pylab as plt # Additional Python plotting utilities
from SBviper.viper_dynamic.collection_time_series import TimeSeriesCollection
from SBviper.viper_dynamic.time_series import TimeSeries
from SBviper.viper_helpers.derivative_dtw import DerivativeDTW

original_model = te.loada("/Users/stevema/Desktop/Research/SBviper/tests/experiments/model_ant_original.txt")
revised_model = te.loada("/Users/stevema/Desktop/Research/SBviper/tests/experiments/model_ant_revised.txt")

# original import
original_result = original_model.simulate(0, 100, 1000, ["time", "oxy"])
original_tsc = TimeSeriesCollection.from_nd_array(original_result)
original_ts_oxy = original_tsc.get_time_series("oxy")
original_ts_oxy_timep = original_ts_oxy.time_points
original_ts_oxy_val = original_ts_oxy.values

# revised import
revised_result = revised_model.simulate(0, 100, 1000, ["time", "oxy"])
revised_tsc = TimeSeriesCollection.from_nd_array(revised_result)
revised_ts_oxy = revised_tsc.get_time_series("oxy")
revised_ts_oxy_timep = revised_ts_oxy.time_points
revised_ts_oxy_val = revised_ts_oxy.values

# test derivative dtw
dtw_calculator = DerivativeDTW(original_ts_oxy, revised_ts_oxy)
print(dtw_calculator.compute())
dtw_calculator.plot_derivative()

# testing own sbml

# random testing
# ts1 = TimeSeries("one", np.array([1, 2, 3, 4]), np.array([1, 2, 3, 4]))
# ts2 = TimeSeries("two", np.array([2, 4, 6, 8]), np.array([1, 2, 3, 4]))
# plt.plot(ts1.values, ts1.time_points)
# plt.plot(ts2.values, ts2.time_points)
# plt.show()
# dtw_calculator = DerivativeDTW(ts1, ts2)
# print(dtw_calculator.compute())
