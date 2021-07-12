from functools import reduce
from .controller import Controller


class VariableDerivative(Controller):
    name = 'VariableDerivative'

    def __init__(self, arguments):
        super().__init__(arguments)
        self.varToDiff, self.varWithRespectTo = arguments

    def toTex(self, needsBrackets=False, environment=False):
        mainTex = "\\frac{d}{d"+self.variable.toTex()+"}(" + \
            self.function.toTex()+")"
        if(needsBrackets):
            return "("+mainTex+")"
        else:
            return mainTex
