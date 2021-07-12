from functools import reduce
from .controller import ControllerWithInner
import math


class TanController(ControllerWithInner):
    name = 'Tan'

    def differentiate(self, VarName):
        return self.inner.sec()**2*self.inner.differentiate(VarName)

    def toTex(self, needsBrackets=False, environment=False):
        return '\\tan('+self.inner.toTex()+')'

    def evaluate(self):
        return math.tan(self.inner.evaluate())
