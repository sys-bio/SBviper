"""Test case implementation"""

import unittest


class TestCase(unittest.TestCase):

    def assertParameterInit(self, sbml):
        """
        Checks whether the parameter values have been initialized
        Parameter values are considered unset if a model does not contain
        a setting for the "value" attribute of a parameter, nor does it has
        a default value
        :param sbml: a simple_sbml representation of the sbml model
        :return: True iff all of the parameters have been initialized
        """
        for parameter in sbml.parameters:
            super().assertTrue(parameter.isSetValue())

    def assertNotNegative(self, sbml):
        # TODO: implement assertNotNegative
        pass
