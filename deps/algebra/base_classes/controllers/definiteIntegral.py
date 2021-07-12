from functools import reduce
from .controller import Controller


class DefiniteIntegralController(Controller):
    name = 'DefiniteIntegral'

    def __init__(self, arguments):
        super().__init__(arguments)
        self.lowerBound, self.upperBound, self.integrand, self.variable = arguments

    def differentiate(self, VarName):
        if VarName == self.variable.getName():
            return self.integrand
        else:
            return 0

    def toTex(self, needsBrackets=False, environment=False):
        mainTex = '\int_{ '+self.lowerBound.toTex()+' }^{ '+self.upperBound.toTex()+' }' + \
            self.integrand.toTex()+'d'+self.variable.toTex()
        if(needsBrackets):
            return "("+mainTex+")"
        else:
            return mainTex

    def canCalculate(self):
        return False
