from functools import reduce
from .controller import Controller


class DerivativeController(Controller):
    name = 'Derivative'

    def __init__(self, arguments):
        super().__init__(arguments)
        self.variable, self.function = arguments

    def toTex(self, needsBrackets=False, environment=False):
        mainTex = "\\frac{d}{d"+self.variable.toTex()+"}(" + \
            self.function.toTex()+")"
        if(needsBrackets):
            return "("+mainTex+")"
        else:
            return mainTex

    def differentiate(self, varName):
        raise Exception("Cannot differentiate derivatives, sorry!")