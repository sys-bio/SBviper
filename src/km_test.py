"""
Static tests for kinetic models
Arguments:
    path to an XML file
    option [Basics, ...]
"""

import unittest
import sys
from simple_sbml.simple_sbml import SimpleSBML
from util import getABSPath

def printHeader(header):
    """
    Prints the header in a somewhat non-ungly format
    :param header: the header we're printing out
    """
    print("==================================================")
    print(header)
    print("==================================================")


class StaticTestCase(unittest.TestCase):
    sbml = None

    @classmethod
    def init(cls, path_to_xml, option):
        """
        Initializes a simple_sbml object for the test and run
        categories of tests accordingly
        :param path_to_xml: the path to a XML representation of the model
        :param option: test categories to run
                       - [Basic]: basic static tests for the model
        """
        abs_path_to_xml = getABSPath(path_to_xml)
        cls.sbml = SimpleSBML(abs_path_to_xml)
        if option == "Basic":
            cls.runBasicTests()
        else:
            cls.Usage()

    @classmethod
    def Usage(cls):
        """
        Prints the usage and exit
        """
        print("usage: km_test.py path_to_XML [option]")
        print("[option]: Basic")
        exit(1)

    @classmethod
    def runBasicTests(cls):
        """
        runs the basic tests and print out errors accordingly
        :return:
        """
        cls.assertParameterInit(cls.sbml)

    @staticmethod
    def assertParameterInit(sbml):
        """
        Checks whether the parameter values have been initialized
        Parameter values are considered unset if a model does not contain
        a setting for the "value" attribute of a parameter, nor does it has
        a default value
        :param sbml: a simple_sbml representation of the model
        """
        # iterate through all of the parameters
        printHeader("PARAMETER INITIALIZATION")
        error = 0
        for parameter in sbml.parameters:
            if not parameter.isSetValue():
                error += 1
                print(parameter.getName() + " is uninitialized!\n")
        print("TOTAL ERROR FOUND: " + str(error) + "\n")

    @staticmethod
    def assertParameterValNotZero(sbml):
        """
        Checks whether the parameter value is initialized, and is a non-zero number
        :param sbml: a simple_sbml representation of the model
        :param an_id: string representation of the id
        :return: True iff the value is initialized, and is a non-zero number
                 False iff the value is initialized, but is set to zero
                 None if the value is not initialized
        """
        for parameter in sbml.parameters:
            if not parameter.isSetValue():
                return None
            elif parameter.getValue() == 0:
                return False
        return True

    @staticmethod
    def assertSpeciesInit(sbml):
        """
        Checks whether the values of all chemical species referenced in a
        kinetics law has been initialized
        :param sbml: a simple_sbml representation of the model
        :return: True iff all of the species referenced in the kinetics law
                 has been initialized
        """
        reactions = sbml.reactions  # get all of the reactions involved
        for reaction in reactions:
            # get all of the parameters' and species' names involved in the reaction
            symbols = reaction.kinetic_law._getSymbols()
            for symbol in symbols:
                species = sbml.getSpecies(symbol)
                # skip all of the parameters, see assertParameterInit for parameter testing
                if species is None:
                    continue
                if not species.isSetInitialConcentration() and not species.isSetInitialAmount():  # initial amount
                    return False
        return True

    # kinetics expression
    # A + B -> C; k1*A*B, mass action
    # A + B + C -> D; k1*A*B, counter
    # A + B -> C; k1*C, c starts non-zero, or another action in place
    # symbols -> also reactants in the reaction and all reactants in the reaction are symbols
    # could be exceptions
    # warnings and failures

    # networkx


if __name__ == "__main__":
    if len(sys.argv) == 2:
        # set the option to "basic" as default
        StaticTestCase.init(sys.argv[1], "Basic")
    elif len(sys.argv) == 3:
        StaticTestCase.init(sys.argv[1], sys.argv[2])
    else:
        StaticTestCase.Usage()
