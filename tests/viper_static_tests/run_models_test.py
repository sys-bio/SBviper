import os
from simple_sbml.simple_sbml import SimpleSBML
from viper_static.viper_static import ViperStatic

directory = "/Users/mabochen/Desktop/Research/SBViper/examples/biomodels"

total = 0
warning = 0
names = []

for filename in os.listdir(directory):
    if filename.endswith(".xml"):
        print(filename)
        abs_path_file = directory + "/" + filename
        sbml = None
        try:
            sbml = SimpleSBML(abs_path_file)
        except (ValueError, IOError, AttributeError) as e:
            continue
        tester = ViperStatic(sbml)
        missing = tester.assert_parameter_init()
        total += 1
        if len(missing) > 0:
            names.append(filename)
            warning += 1
print("Total: " + str(total))
print("# of Warning models: " + str(warning))
print("Warning models: " + str(names))
