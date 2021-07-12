from .AdvancedRule import AdvancedRule
from ..base_classes.base import *


class FunctionalRule(AdvancedRule):
    def __init__(self, head, prerequisites, function, name, trivial=False):
        self.head = head
        self.function = function
        self.trivial = trivial
        self.prerequisites = prerequisites
        self.name = name

    def apply(self, expression, targetVariable=False):
        unification = self.getUnification(expression)
        if unification == {} or (unification != None and unification != False):
            
            result = self.function(expression, unification)
            if result != False:
                return result
        return False

    def toTex(self):
        return "\\text{"+str(self.name)+"}"
