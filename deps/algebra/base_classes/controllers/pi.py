from .controller import Controller
import math


class PiController(Controller):
    name = "Pi"

    def toTex(self, needsBrackets=False, environment=False):
        return '\\pi '

    def differentiate(self, VarName):
        return 0

    def canCalculate(self):
        return False

    def evaluate(self):
        return math.pi