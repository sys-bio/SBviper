"""
Static tests for kinetic models
"""

import sys
import unittest
import networkx as nx
from simple_sbml.simple_sbml import SimpleSBML
from util import get_abs_path
import matplotlib.pyplot as plt


# TODO: clean up
def print_header(header):
    """
    Prints the header in a somewhat non-ungly format
    :param header: the header we're printing out
    """
    print("==========================================================")
    print(header)
    print("----------------------------------------------------------")


def print_footer(msg):
    """
    Prints the footer
    """
    print(msg)
    print("==========================================================\n")


def speciesrefs_to_strs(srs):
    """
    Converts a list of species references to a list of string representation of species
    :param srs: list of species references
    :return: list of string representation of the species
    """
    res = []
    for reactant in srs:
        res.append(reactant.species)
    return res


def species_to_strs(species):
    """
    :return: a list of species in string representation
    """
    res = []
    for specie in species:
        res.append(specie.getId())
    return res


def speciesrefs_to_concatstr(srs):
    """
    given a list of species reference, concatenate the list to a string representation separated by "-"
    :param srs: target list of species reference
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


def print_reaction_graph(sbml):
    """
    prints the reaction graph
    :param sbml: the sbml model in simple_sbml format
    """
    graph = nx.DiGraph()
    for reaction in sbml.reactions:
        reactants = reaction.reactants  # reactants of the reaction
        products = reaction.products  # products of the reaction
        reactants_str = speciesrefs_to_concatstr(reactants)
        products_str = speciesrefs_to_concatstr(products)
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
    # output the graph
    options = {
        'node_color': 'black',
        'node_size': 5,
        'width': 1,
    }
    nx.draw(graph, with_labels=True, **options)
    plt.show()


def get_initialized_species(species):
    """
    :param species: a list of species in the model
    :return: return a set of initialized species in string format
    """
    res = set()
    for s in species:
        if s.isSetInitialAmount() or s.isSetInitialConcentration():
            res.add(s.getId())
    return res


def is_entry_node(species_list, init_species):
    """
    Checks whether the species in the list is initialized
    :param species_list: list of species references
    :param init_species: list of initialized species for the reaction
    :return: true iff all of the species in the list is initialized
    """
    for species in species_list:
        if species.species not in init_species:
            return False
    return True


class StaticTestCase(unittest.TestCase):

    def __init__(self, sbml):
        """
        Initializes a simple_sbml object for the test and run
        categories of tests accordingly
        :param sbml: the sbml model in simple_sbml representation
        """
        super().__init__()
        self.sbml = sbml

    def run_basic_tests(self):
        """
        runs the basic tests and print out errors accordingly
        """
        self.basic_param_checks()
        self.basic_species_checks()
        self.basic_reaction_checks()

    def basic_param_checks(self):
        self.assert_parameter_init()
        self.assert_parameter_val_not_zero()

    def basic_species_checks(self):
        self.assert_species_init()

    def basic_reaction_checks(self):
        self.assert_reactants_in_kinetics()
        self.reach_all_species()

    def assert_parameter_init(self):
        """
        Checks whether the parameter values have been initialized
        Parameter values are considered unset if a model does not contain
        a setting for the "value" attribute of a parameter, nor does it has
        a default value
        :return a list of uninitialized parameter objects
        """
        # iterate through all of the parameters
        print_header("All parameters should be initialized.")
        missing = []
        error = 0
        for parameter in self.sbml.parameters:
            # self.assertTrue(parameter.isSetValue, "ERROR: " + parameter.getId() + " is uninitialized!")
            if not parameter.isSetValue():
                error += 1
                missing.append(parameter)
                print("ERROR: " + parameter.getId() + " is UNINITIALIZED!")
        print_footer("ERRORS FOUND: " + str(error))
        return missing

    def assert_parameter_val_not_zero(self):
        """
        Checks whether the initialized parameter value is a non-zero number
        runs after checking parameter initialization
        :return a list of parameter objects with value zero
        """
        print_header("Parameter value should not be set to ZERO.")
        missing = []
        error = 0
        for parameter in self.sbml.parameters:
            if parameter.isSetValue() and parameter.getValue() == 0:
                error += 1
                missing.append(parameter)
                print("WARNING: " + parameter.getId() + " is set to ZERO!")
        print_footer("WARNINGS FOUND: " + str(error))
        return missing

    def assert_species_init(self):
        """
        Checks whether the values of all chemical species referenced in a
        kinetics law has been initialized
        :return: a list of species objects with uninitialized values in kinetics law
        """
        print_header("Species concentration / initial amount should be initialized.")
        missing = []
        error = 0
        reactions = self.sbml.reactions  # get all of the reactions involved
        for reaction in reactions:
            # get all of the parameters' and species' names involved in the reaction
            symbols = reaction.kinetic_law._getSymbols()
            for symbol in symbols:
                species = self.sbml.get_species(symbol)
                # skip all of the parameters, see assertParameterInit for parameter testing
                if species is None:
                    continue
                if not species.isSetInitialConcentration() and not species.isSetInitialAmount():  # initial amount
                    error += 1
                    missing.append(species)
                    print("WARNING: " + species.getId() + " is UNINITIALIZED")
        print_footer("WARNINGS FOUND: " + str(error))
        return missing

    def assert_reactants_in_kinetics(self):
        """
        Checks whether all reactant species are referenced in the kinetics law,
        and the kinetics law only references reactant species
        :return: a list of reaction that does not satisfy the above condition
        """
        print_header("All reactants should be in the kinetics law, \nand all species references in the kinetics law \n"
                     "should be reactants.")  # wtf is this
        missing = []
        error = 0
        for reaction in self.sbml.reactions:
            kn_symbols = set(reaction.kinetic_law.symbols)  # set of str
            reactants = set(
                speciesrefs_to_strs(reaction.reactants))  # list of speciesReference -> list of str -> set
            react = None
            # check whether all species references in the kinetics law is a reactant
            for symbol in kn_symbols:
                species = self.sbml.get_species(symbol)
                if species is None:  # is not a species
                    continue
                if symbol not in reactants:
                    error += 1
                    react = reaction
                    print("WARNING: In reaction " + reaction.id + ", " + species.getId() +
                          " is found in the kinetics law, but is NOT a reactant")
            # check whether all reactants are references in kinetics law
            for reactant in reactants:
                species = self.sbml.get_species(reactant)
                if reactant not in kn_symbols:
                    error += 1
                    react = reaction
                    print("WARNING: In reaction " + reaction.id + ", " + species.getId() +
                          " is found as a reactant, but NOT referenced in the Kinetics law")
            if react is not None:
                missing.append(react)
        print_footer("WARNINGS FOUND: " + str(error))
        return missing

    def reach_all_species(self):
        """
        Checks whether all species are reachable through the chain of reactions
        The entry of the reaction is defined to be:
        - initialized amount or concentration
        :return: a list of species objects that are unreachable
        """
        # TODO: add return value
        print_header("All species should be reachable in the reactions")
        missing = []
        error = 0
        graph = nx.DiGraph()  # a representation of the graph
        all_node = set()  # all of the nodes in the graph, in string format
        entry_node = set()  # all of the entry nodes in the graph
        init_species = get_initialized_species(self.sbml.species)  # all species that are initialized
        # create the graph
        for reaction in self.sbml.reactions:
            reactants = reaction.reactants  # reactants of the reaction
            products = reaction.products  # products of the reaction
            reactants_str = speciesrefs_to_concatstr(reactants)
            products_str = speciesrefs_to_concatstr(products)
            # add the nodes and edges to the graph
            if len(reactants) > 0 and len(products) > 0:
                if not graph.__contains__(reactants_str):
                    if is_entry_node(reactants, init_species):
                        entry_node.add(reactants_str)
                    all_node.add(reactants_str)
                    graph.add_node(reactants_str)
                if not graph.__contains__(products_str):
                    if is_entry_node(products, init_species):
                        entry_node.add(products_str)
                    all_node.add(products_str)
                    graph.add_node(products_str)
                graph.add_edge(reactants_str, products_str)
            elif len(reactants) > 0 and not graph.__contains__(reactants_str) > 0:
                # if the list of reactants is not empty, and the node has not yet been added
                if is_entry_node(reactants, init_species):
                    entry_node.add(reactants_str)
                all_node.add(reactants_str)
                graph.add_node(reactants_str)
            elif len(products) > 0 and not graph.__contains__(products_str) > 0:
                # if the list of products is not empty, and the node has not yet been added
                if is_entry_node(products, init_species):
                    entry_node.add(products_str)
                all_node.add(products_str)
                graph.add_node(products_str)
        # traversing the graph through initialized species
        visited = set()
        for species in entry_node:
            visited.update(set(nx.dfs_postorder_nodes(graph, source=species)))
        # check whether all of the nodes are reached
        for node in all_node:
            if node not in visited:
                print("WARNING: " + node + " is unreachable!")
                error += 1
                # add to return list
                strings = node.split("-")
                for string in strings:
                    missing.append(self.sbml.str_to_species(string))
        print_footer("WARNINGS FOUND: " + str(error))
        return missing
