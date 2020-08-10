"""Test case implementation"""

import unittest


class StaticTestCase(unittest.TestCase):

    def assertParameterInit(self, sbml):
        """
        Checks whether the parameter values have been initialized
        Parameter values are considered unset if a model does not contain
        a setting for the "value" attribute of a parameter, nor does it has
        a default value
        :param sbml: a simple_sbml representation of the model
        :return: True iff all of the parameters have been initialized
        """
        # iterate through all of the parameters
        for parameter in sbml.parameters:
            self.assertTrue(parameter.isSetValue())

    def assertSpeciesInit(self, sbml):
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
                self.assertTrue(species.isSetInitialConcentration())
