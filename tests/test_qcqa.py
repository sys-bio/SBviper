import mass.test
from mass import MassConfiguration
from mass.util import qcqa
from mass.io import sbml
from os.path import join


a = sbml.read_sbml_model("/Users/mabochen/Desktop/Research/SBViper/examples/test_examples/test_file.xml")

qcqa.qcqa_model(
    a,
    parameters=True,        # Check for undefined but necessary parameters in the model
    concentrations=True,    # Check for undefined but necessary concentrations in the model
    fluxes=True,            # Check for undefined steady state fluxes for reactions in the model
    superfluous=True,       # Check for excess parameters and ensure they are consistent.
    elemental=True,         # Check mass and charge balancing of reactions in the model
    simulation_only=True,  # Check for values necessary for simulation only
)