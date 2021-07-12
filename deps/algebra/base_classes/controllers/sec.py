from functools import reduce
from .controller import ControllerWithInner
import math


class SecController(ControllerWithInner):
    name = 'Sec'

    def differentiate(self, VarName):
        return self.inner.sec()*self.inner.tan()

    def toTex(self, needsBrackets=False, environment=False):
        return '\\sec('+self.inner.toTex()+')'

    def evaluate(self):
        return 1/math.cos(self.inner.evaluate())
