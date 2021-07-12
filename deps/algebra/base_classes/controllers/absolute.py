from functools import reduce
from .controller import Controller, ControllerWithInner
import math


class AbsController(ControllerWithInner):
    name = 'Abs'

    def differentiate(self, VarName):
        raise Exception("Cannot differentiate absolute values")

    def toTex(self, needsBrackets=False, environment=False):
        return '|'+self.inner.toTex()+'|'

    def evaluate(self):
        return abs(self.inner.evaluate())
