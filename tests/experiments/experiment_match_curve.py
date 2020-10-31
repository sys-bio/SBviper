import tellurium as te # Python-based modeling environment for kinetic models
import tkinter
import roadrunner as rr # High-performance simulation and analysis library
import numpy as np # Scientific computing package
import random # Generate random numbers
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pylab as plt # Additional Python plotting utilities
from SBviper.viper_dynamic.collection_time_series import TimeSeriesCollection

# model = te.loadSBMLModel("/Users/stevema/Desktop/Research/SBviper/examples/biomodels/BIOMD0000000090.xml")
# model.exportToAntimony("model_ant_original.txt", current=True)

original_model = te.loada("/Users/stevema/Desktop/Research/SBviper/tests/experiments/model_ant_original.txt")

# model.plot(figsize = (10, 6), xtitle = 'Time', ytitle = 'Concentration')
original_result = original_model.simulate(0, 100, 1000, ['time', 'oxy'])
original_tsc = TimeSeriesCollection.from_nd_array(original_result)
