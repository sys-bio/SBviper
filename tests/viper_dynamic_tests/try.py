import tellurium as te
import roadrunner as rr
import numpy as np
import random
import matplotlib.pylab as plt
import unittest

from SBviper.viper_dynamic.collection_time_series import TimeSeriesCollection
from SBviper.viper_dynamic.collection_time_series import TimeSeries

ant_str = """
model test               # name the model
    compartment C1;      # specify compartments
    C1 = 1.0;            # assign compartment volume
    species S1, S2;      # specify species
    S1 in C1; S2 in C1;  # allocate species to appropriate compartment


    J1: S1 -> S2; k1; # reaction; reaction rate law;

    S1 = 10.0;           # assign species initial conditions
    S2 = 0.0;

    k1 = 1.0;            # assign constant values to global parameters
end
"""
r = te.loada(ant_str)
result = r.simulate(0, 10, 25)
tsc = TimeSeriesCollection.from_nd_array(result)
s1ts = tsc.get_time_series("S1")
print(s1ts.values)
print(s1ts.time_points)
print(s1ts.get_value_at_time(0.41666667))
