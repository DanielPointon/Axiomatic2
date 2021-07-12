from .controller import Controller
import math


class ComplexUnitController(Controller):
    name = "Complex"

    def toTex(self, needsBrackets=False, environment=False):
        return 'i'

    def differentiate(self, VarName):
        return 0

    def canCalculate(self):
        return False
