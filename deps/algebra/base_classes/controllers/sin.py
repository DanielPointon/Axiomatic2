from functools import reduce
from .controller import ControllerWithInner
import math


class SinController(ControllerWithInner):
    name = 'Sin'

    def differentiate(self, VarName):
        return self.inner.cos()*self.inner.differentiate(VarName)

    def toTex(self, needsBrackets=False, environment=False):
        return '\\sin('+self.inner.toTex()+')'

    def evaluate(self):
        return math.sin(self.inner.evaluate())
