from functools import reduce
from .controller import Controller


class IndefiniteIntegralController(Controller):
    name = 'IndefiniteIntegral'

    def __init__(self, arguments):
        self.function, self.variable = arguments

    def differentiate(self, VarName):
        if VarName == self.variable.getName():
            return self.function
        else:
            raise Exception("Cannot diff")

    def toTex(self, needsBrackets=False, environment=False):
        functionTex=self.function.toTex()
        if not self.function.isSingleTerm():
            mainTex = '\int ('+functionTex+') \\space d'+self.variable.toTex()
        else:
            mainTex = '\int '+functionTex+' \\space d'+self.variable.toTex()
        if(needsBrackets):
            return "("+mainTex+")"
        else:
            return mainTex

    def canCalculate(self):
        return False
