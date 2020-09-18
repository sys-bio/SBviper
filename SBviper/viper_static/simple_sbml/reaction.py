'''Python Abstraction for a Reaction.'''

from simple_sbml import constants as cn
from simple_sbml.kinetic_law import KineticLaw
from simple_sbml import util

import numpy as np
import libsbml


class Reaction(object):

  def __init__(self, libsbml_reaction):
    """
    :param libsbml.Reaction libsbml_reaction:
    """
    self.reaction = libsbml_reaction
    # List of species reference
    self.reactants =  [self.reaction.getReactant(n)
        for n in range(self.reaction.getNumReactants())]
    # List of species reference
    self.products =  [self.reaction.getProduct(n)
        for n in range(self.reaction.getNumProducts())]
    self.kinetic_law = KineticLaw(
        self.reaction.getKineticLaw(), self)
    self.id = self.reaction.getId()

  def getId(self):
    return self.id
