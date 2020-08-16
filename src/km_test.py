"""
Static tests for kinetic models
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
    print("--------------------------------------------------")


def printFooter(msg):
    """
    Prints the footer
    """
    print(msg)
    print("==================================================\n")


def Usage():
    """
    Prints the usage and exit
    """
    print("usage: km_test.py path_to_XML [option]")
    print("[option]: Basic")
    exit(1)


def speciesRefToSpecies(reactants):
    res = []
    for reactant in reactants:
        res.append(reactant.species)
    return res


class StaticTestCase(unittest.TestCase):

    def __init__(self, path_to_xml, option):
        """
        Initializes a simple_sbml object for the test and run
        categories of tests accordingly
        :param path_to_xml: the path to a XML representation of the model
        :param option: test categories to run
                       - [Basic]: basic static tests for the model
        """
        super().__init__()
        abs_path_to_xml = getABSPath(path_to_xml)
        self.sbml = SimpleSBML(abs_path_to_xml)
        if option == "Basic":
            self.runBasicTests()
        else:
            Usage()

    def runBasicTests(self):
        """
        runs the basic tests and print out errors accordingly
        """
        self.basicParamChecks()
        self.basicSpeciesChecks()
        self.basicReactionChecks()

    def basicParamChecks(self):
        self.assertParameterInit()
        self.assertParameterValNotZero()

    def basicSpeciesChecks(self):
        self.assertSpeciesInit()

    def basicReactionChecks(self):
        self.assertReactantsInKinetics()

    def assertParameterInit(self):
        """
        Checks whether the parameter values have been initialized
        Parameter values are considered unset if a model does not contain
        a setting for the "value" attribute of a parameter, nor does it has
        a default value
        :param sbml: a simple_sbml representation of the model
        :return a list of uninitialized parameter objects
        """
        # iterate through all of the parameters
        printHeader("PARAMETER INITIALIZATION")
        missing = []
        error = 0
        for parameter in self.sbml.parameters:
            # self.assertTrue(parameter.isSetValue, "ERROR: " + parameter.getId() + " is uninitialized!")
            if not parameter.isSetValue():
                error += 1
                missing.append(parameter)
                print("ERROR: " + parameter.getId() + " is uninitialized!")
        printFooter("ERRORS FOUND: " + str(error))
        return missing

    def assertParameterValNotZero(self):
        """
        Checks whether the initialized parameter value is a non-zero number
        runs after checking parameter initialization
        :param sbml: a simple_sbml representation of the model
        :param an_id: string representation of the id
        :return a list of parameter objects with value zero
        """
        printHeader("PARAMETER VALUE NOT ZERO")
        missing = []
        error = 0
        for parameter in self.sbml.parameters:
            if parameter.isSetValue() and parameter.getValue() == 0:
                error += 1
                missing.append(parameter)
                print("WARNING: " + parameter.getId() + " is set to ZERO!")
        printFooter("WARNINGS FOUND: " + str(error))
        return missing

    def assertSpeciesInit(self):
        """
        Checks whether the values of all chemical species referenced in a
        kinetics law has been initialized
        :param sbml: a simple_sbml representation of the model
        :return: a list of species objects with uninitialized values in kinetics law
        """
        printHeader("SPECIES INITIALIZATION")
        missing = []
        error = 0
        reactions = self.sbml.reactions  # get all of the reactions involved
        for reaction in reactions:
            # get all of the parameters' and species' names involved in the reaction
            symbols = reaction.kinetic_law._getSymbols()
            for symbol in symbols:
                species = self.sbml.getSpecies(symbol)
                # skip all of the parameters, see assertParameterInit for parameter testing
                if species is None:
                    continue
                if not species.isSetInitialConcentration() and not species.isSetInitialAmount():  # initial amount
                    error += 1
                    missing.append(species)
                    print("WARNING: " + species.getId() + " is uninitialized")
        printFooter("WARNINGS FOUND: " + str(error))
        return missing

    def assertReactantsInKinetics(self):
        """
        Checks whether all reactant species are referenced in the kinetics law,
        and the kinetics law only references reactant species
        :return: a list of reaction that does not satisfy the above condition
        """
        printHeader("REACTANTS IN KINETICS LAW")
        missing = []
        error = 0
        reactions = self.sbml.reactions
        for reaction in reactions:
            symbols = reaction.kinetic_law.symbols  # list of str
            reactants = speciesRefToSpecies(reaction.reactants)  # list of speciesReference -> list of str
            react = None
            for symbol in symbols:
                species = self.sbml.getSpecies(symbol)
                if species is None:  # is not a species
                    continue
                if symbol not in reactants:
                    error += 1
                    react = reaction
                    print("WARNING: " + species.getId() + " is found in the kinetics law, but is not a reactant")
            for reactant in reactants:
                if reactant not in symbols:
                    error += 1
                    react = reaction
                    print("WARNING: " + reactant.getId() + " is found as a reactant, but not referenced in the "
                                                           "Kinetics law")
            if react is not None:
                missing.append(react)
        printFooter("WARNINGS FOUND: " + str(error))
        return missing


    # kinetics expression
    # A + B -> C; k1*A*B, mass action
    # A + B + C -> D; k1*A*B, counter
    # A + B -> C; k1*C, c starts non-zero, or another action in place
    # symbols -> also reactants in the reaction and all reactants in the reaction are symbols
    # could be exceptions
    # warnings and failures

    # networkx
