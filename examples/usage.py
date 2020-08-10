"""Example for using the testing framework"""

from src import km_test
from tests import helpers


class Usage(km_test.TestCase):

    def setUp(self):
        self.SBML = helpers.getSimple()

    def testParameterInit(self):
        """
        Testing whether all of the parameters have set values
        """
        # calls the method from the super class that checks for initialization
        return super().assertParameterInit(self.SBML)
