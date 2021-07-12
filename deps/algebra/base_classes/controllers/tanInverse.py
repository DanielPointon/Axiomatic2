from .controller import ControllerWithInner
import math


class ArcTanController(ControllerWithInner):
    name = "ArcTan"

    def toTex(self, needsBrackets=False, environment=False):
        return '\\tan^{-1}('+self.inner.toTex()+')'

    def evaluate(self):
        return math.atan(self.inner.evaluate())

    def differentiate(self, VarName):
        return (self.inner.differentiate(VarName))/((self.inner**2)+1)
