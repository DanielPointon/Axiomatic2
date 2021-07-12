from .controller import ControllerWithInner
import math


class ArcCosController(ControllerWithInner):
    name = "ArcCos"

    def toTex(self, needsBrackets=False, environment=False):
        return '\\cos^{-1}('+self.inner.toTex()+')'

    def evaluate(self):
        return math.acos(self.inner.evaluate())

    def differentiate(self, VarName):
        return -1*(self.inner.differentiate(VarName))/((1-self.inner**2)**0.5)

    def canCalculate(self):
        return self.inner.canCalculate() and -1 <= self.inner.evaluate() and self.inner.evaluate() <= 1
