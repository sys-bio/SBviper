import os
import util as ut
from simple_sbml.simple_sbml import SimpleSBML
from km_test import StaticTestCase

directory = "/Users/mabochen/Desktop/Research/km_test/examples/biomodels"

total = 0
warning = 0

for filename in os.listdir(directory):
    if filename.endswith(".xml"):
        print(filename)
        abs_path_file = directory + "/" + filename
        sbml = None
        try:
            sbml = SimpleSBML(abs_path_file)
        except (ValueError, IOError, AttributeError) as e:
            continue
        tester = StaticTestCase(sbml)
        missing = tester.assert_reactants_in_kl()
        total += 1
        if len(missing) > 0:
            warning += 1
print("Total: " + str(total))
print("Warning models: " + str(warning))
