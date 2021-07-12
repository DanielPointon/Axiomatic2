from functools import reduce
from .controller import Controller, ControllerWithInner
import math


class CosController(ControllerWithInner):
    name = 'Cos'

    def differentiate(self, VarName):
        return -1*self.inner.sin()*self.inner.differentiate(VarName)

    def toTex(self, needsBrackets=False, environment=False):
        return '\\cos('+self.inner.toTex()+')'

    def evaluate(self):
        return math.cos(self.inner.evaluate())
