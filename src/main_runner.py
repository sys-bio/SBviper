"""
Runner for km_test
Arguments:
    an XML filename
    option [Basics, ...]
"""

import argparse
import os.path
import util as ut
from simple_sbml.simple_sbml import SimpleSBML
import logging
from km_test import StaticTestCase


def check_valid_file(file):
    if not os.path.exists(file):
        parser.error("The file %s does not exist!" % file)
    elif not file.endswith(".xml"):
        parser.error("The file %s is not a valid XML file!" % file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Static test for Kinetics Models in System Biology")
    # argument for the filename of the model
    parser.add_argument("F", type=str,
                        help="The name for the XML file under the current directory")
    # argument for the test mode
    # only implemented "Basics" for now
    list_choices = ["basics", "kinetics"]
    parser.add_argument("-m", "--mode", type=str, nargs="?", default="basics",
                        help="Test mode for the model (default: basics)", choices=list_choices)
    args = parser.parse_args()
    filename = args.F  # the name of the XML file of the model
    # check if the file exists and if it is an XML file
    check_valid_file(filename)
    mode = args.mode  # option for the mode of the test, defaulted to be basics
    # create an simple_sbml representation of the model
    # get the absolute path
    abs_path_file = ut.get_abs_path(filename)
    sbml = None
    try:
        sbml = SimpleSBML(abs_path_file)
    except (ValueError, IOError) as e:
        parser.error("Error encountered: %s" % str(e))
    # create the tester
    tester = StaticTestCase(sbml)
    if mode == "basics" or mode == "kinetics":
        tester.runBasicTests()
