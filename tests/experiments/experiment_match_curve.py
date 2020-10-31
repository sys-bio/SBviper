import tellurium as te # Python-based modeling environment for kinetic models
import tkinter
import roadrunner as rr # High-performance simulation and analysis library
import numpy as np # Scientific computing package
import random # Generate random numbers
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pylab as plt # Additional Python plotting utilities

# model = te.loadSBMLModel("/Users/stevema/Desktop/Research/SBviper/examples/biomodels/BIOMD0000000090.xml")
# model.exportToAntimony("model_ant_original.txt", current=True)

model = te.loada("/Users/stevema/Desktop/Research/SBviper/tests/experiments/model_ant_original.txt")

model.simulate(0, 100, 1000, ['time', 'oxy'])
# model.plot(figsize = (10, 6), xtitle = 'Time', ytitle = 'Concentration')

