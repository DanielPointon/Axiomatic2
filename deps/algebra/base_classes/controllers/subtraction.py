from .controller import Controller


class SubtractionController(Controller):
    name = 'Subtraction'

    def __init__(self, arguments):
        super().__init__(arguments)
        self.expression, self.subtractor, = arguments

    def evaluate(self):
        return self.arguments[0].evaluate()-self.arguments[1].evaluate()

    def differentiate(self, VarName):
        return self.expression.differentiate(VarName)-self.subtractor.differentiate(VarName)

    def toTex(self, needsBrackets=False, environment=False):
        mainTex = self.expression.toTex(True)+'-'+self.subtractor.toTex(True)
        if(needsBrackets):
            return "("+mainTex+")"
        else:
            return mainTex
