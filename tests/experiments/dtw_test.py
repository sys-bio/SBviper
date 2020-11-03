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

# test fast dtw
distance, path = fastdtw(original_ts_oxy_val, revised_ts_oxy_val, dist=euclidean)
print(distance)

distance, path = fastdtw([1,2,3,4,5], [0,0,1,2,3,4,5], dist=euclidean)
print(distance)

# test derivative dtw