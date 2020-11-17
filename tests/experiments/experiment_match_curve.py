# Testing how the changes in the model changes the behavior of the concentration of oxygen

import tellurium as te # Python-based modeling environment for kinetic models
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pylab as plt # Additional Python plotting utilities
from viper_dynamic.time_series.collection_time_series import TimeSeriesCollection

# model = te.loadSBMLModel("/Users/stevema/Desktop/Research/SBviper/examples/biomodels/BIOMD0000000090.xml")
# model.exportToAntimony("model_ant_original.txt", current=True)

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

#plot
plt.plot(original_ts_oxy_timep, original_ts_oxy_val, label="original")
plt.plot(revised_ts_oxy_timep, revised_ts_oxy_val, label="revised")
plt.xlabel("Time")
plt.ylabel("Concentration")
plt.legend()
plt.show()
