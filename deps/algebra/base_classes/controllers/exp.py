import math
from .controller import ControllerWithInner


class ExpController(ControllerWithInner):
    name = 'Exp'

    def evaluate(self):
        return math.exp(self.inner.evaluate())

    def differentiate(self, VarName):
        return self.inner.differentiate(VarName)*self.inner.exp()

    def toTex(self, needsBrackets=False, environment=False):
        return '{e}^{ '+self.inner.toTex(False)+' }'
