from .controller import ControllerWithInner
import math


class FactorialController(ControllerWithInner):
    name = 'Controller'

    def differentiate(self, VarName):
        raise Exception('Cannot differentiate factorial')

    def toTex(self, needsBrackets=False, environment=False):
        return self.inner.toTex()+"!"

    def evaluate(self):
        return int(math.factorial(self.inner.evaluate()))
