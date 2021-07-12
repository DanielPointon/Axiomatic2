from .controller import ControllerWithInner
import math


class LnController(ControllerWithInner):
    name = 'Ln'

    def evaluate(self):
        return math.log(self.inner.evaluate())

    def differentiate(self, VarName):
        return self.inner.differentiate(VarName)*1/self.inner

    def toTex(self, needsBrackets=False, environment=False):
        return '\ln('+self.inner.toTex()+')'

    def canCalculate(self):
        return self.inner.canCalculate() and self.inner.evaluate() > 0
