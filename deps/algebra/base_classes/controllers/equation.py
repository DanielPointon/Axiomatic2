import math
from .controller import Controller


class EquationController(Controller):
    name = 'Equation'
    customEnvironmentStatus = True

    def __init__(self, arguments):
        super().__init__(arguments)
        self.leftHandSide, self.rightHandSide = arguments

    def evaluate(self):
        if(self.leftHandSide.toTex() == self.rightHandSide.toTex()):
            return True
        if (self.leftHandSide.canCalculate() and self.rightHandSide.canCalculate()) and (self.leftHandSide.evaluate() == self.rightHandSide.evaluate()):
            return True
        return False

    def differentiate(self, VarName):
        raise Exception("Cannot differentiate equation")

    def toTex(self, needsBrackets=False, environment=False):
        innerTex = self.leftHandSide.toTex()+"="+self.rightHandSide.toTex()
        if environment:
            return "\\begin{"+environment+"}"+innerTex+"\\end{"+environment+"}"
        else:
            return innerTex

    def canCalculate(self):
        return False
