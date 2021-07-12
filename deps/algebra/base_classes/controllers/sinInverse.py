from .controller import ControllerWithInner
import math


class ArcSinController(ControllerWithInner):
    name = "ArcSin"

    def toTex(self, needsBrackets=False, environment=False):
        return '\\sin^{-1}('+self.inner.toTex()+')'

    def evaluate(self):
        return math.asin(self.inner.evaluate())

    def differentiate(self, VarName):
        return (self.inner.differentiate(VarName))/((1-self.inner**2)**0.5)

    def canCalculate(self):
        return self.inner.canCalculate() and -1 <= self.inner.evaluate() and self.inner.evaluate() <= 1
