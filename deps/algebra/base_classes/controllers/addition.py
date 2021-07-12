from functools import reduce
from .controller import Controller


class AdditionController(Controller):
    name = 'Addition'

    def differentiate(self, VarName):
        return reduce(lambda a, b: a+b.differentiate(VarName), self.arguments, 0)

    def toTex(self, needsBrackets=False, environment=False):
        mainTex = ""
        for i in range(len(self.arguments)):
            argumentTex = self.arguments[i].toTex()
            if i == 0:
                mainTex = argumentTex
            else:
                if argumentTex[0] == "-" or argumentTex[0:3] == "\pm":
                    mainTex += argumentTex
                else:
                    mainTex += "+"+argumentTex
        if(needsBrackets):
            return "("+mainTex+")"
        else:
            return mainTex

    def evaluate(self):
        return reduce(lambda a, b: a+b.evaluate(), self.arguments, 0)
