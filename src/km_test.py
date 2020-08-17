"""
Static tests for kinetic models
"""

"""
Q:
1) output printing, HTMLTestRunner
2) return value
"""

import sys
import unittest
import networkx as nx
from simple_sbml.simple_sbml import SimpleSBML
from util import getABSPath
import matplotlib.pyplot as plt


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


def speciesRefToSpeciesStr(srs):
    """
    Converts a list of species references to a list of string representation of species
    :param reactants: list of species references
    :return: list of string representation of the species
    """
    res = []
    for reactant in srs:
        res.append(reactant.species)
    return res


def speciesToSpeciesStr(species):
    """
    :return: a list of species in string representation
    """
    res = []
    for specie in species:
        res.append(specie.getId())
    return res


def speciesRefToConcatenatedStr(srs):
    """
    given a list of species reference, concatenate the list to a string representation separated by "-"
    :param list: target list of species reference
    :return: concatenated string
    """
    if len(srs) == 0:
        return ""
    elif len(srs) == 1:
        return srs[0].species
    else:
        res = srs[0].species
        for i in range(1, len(srs)):
            res += "-" + srs[i].species
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
        self.reachAllSpecies()

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
        for reaction in self.sbml.reactions:
            kn_symbols = set(reaction.kinetic_law.symbols)  # set of str
            reactants = set(
                speciesRefToSpeciesStr(reaction.reactants))  # list of speciesReference -> list of str -> set
            react = None
            # check whether all species references in the kinetics law is a reactant
            for symbol in kn_symbols:
                species = self.sbml.getSpecies(symbol)
                if species is None:  # is not a species
                    continue
                if symbol not in reactants:
                    error += 1
                    react = reaction
                    print("WARNING: " + species.getId() + " is found in the kinetics law, but is not a reactant")
            # check whether all reactants are references in kinetics law
            for reactant in reactants:
                if reactant not in kn_symbols:
                    error += 1
                    react = reaction
                    print("WARNING: " + reactant.getId() + " is found as a reactant, but not referenced in the "
                                                           "Kinetics law")
            if react is not None:
                missing.append(react)
        printFooter("WARNINGS FOUND: " + str(error))
        return missing

    def reachAllSpecies(self):
        """
        Checks whether all species are reachable through the chain of reactions
        How do we know if a node is the entry to a chain of reactions?

        :return: a list of species objects that are unreachable
        """
        graph = nx.Graph()
        for reaction in self.sbml.reactions:
            reactants = reaction.reactants  # reactants of the reaction
            products = reaction.products  # products of the reaction
            reactants_str = speciesRefToConcatenatedStr(reactants)
            products_str = speciesRefToConcatenatedStr(products)
            # add the nodes and edges to the graph
            if len(reactants) > 0 and len(products) > 0:
                if not graph.__contains__(reactants_str):
                    graph.add_node(reactants_str)
                if not graph.__contains__(products_str):
                    graph.add_node(products_str)
                graph.add_edge(reactants_str, products_str)
            elif len(reactants) > 0 and not graph.__contains__(reactants_str) > 0:
                # if the list of reactants is not empty, and the node has not yet been added
                graph.add_node(reactants_str)
            elif len(products) > 0 and not graph.__contains__(products_str) > 0:
                # if the list of products is not empty, and the node has not yet been added
                graph.add_node(products_str)

        # temp, drawing the graph to figure out the relationships
        options = {
        'node_color': 'black',
        'node_size': 5,
        'width': 1,
        }
        nx.draw(graph, with_labels=True, **options)
        plt.show()
