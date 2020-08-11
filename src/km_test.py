"""Test case implementation"""

import unittest


class StaticTestCase(unittest.TestCase):

    @staticmethod
    def assertParameterInit(sbml):
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
            if not parameter.isSetValue():
                return False
        return True

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
                if not species.isSetInitialConcentration():
                    return False
        return True
