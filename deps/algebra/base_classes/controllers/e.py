from .controller import Controller
import math


class EController(Controller):
    name = "E"

    def toTex(self, needsBrackets=False, environment=False):
        return 'e '

    def differentiate(self, VarName):
        return 0

    def canCalculate(self):
        return False

    def evaluate(self):
        return math.e
