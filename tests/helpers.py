from simple_sbml import SimpleSBML

import os

DIR = os.path.dirname(os.path.abspath(__file__))
TEST_PATH = os.path.join(DIR, "test_file.xml")


def getSimple():
    return SimpleSBML(TEST_PATH)
