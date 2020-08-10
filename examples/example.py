"""Example for using the testing framework"""

from src import km_test
from tests import helpers


class Example(km_test.StaticTestCase):

    def setUp(self):
        self.SBML = helpers.getSimple()

    def testParameterInit(self):
        """
        Testing whether all of the parameters have set values
        """
        # calls the method from the super class that checks for initialization
        return self.assertParameterInit(self.SBML)

    def testSpeciesInit(self):
        """
        Testing whether all of the species referenced in a kinetics law
        has been initialized
        """
        return self.assertSpeciesInit(self.SBML)
