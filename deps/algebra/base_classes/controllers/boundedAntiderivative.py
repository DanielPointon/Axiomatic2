from .controller import Controller


class BoundedAntiDerivativeController(Controller):
    name = 'BoundedAntiDerivative'

    def __init__(self, arguments):
        super().__init__(arguments)
        self.function, self.variable, self.lowerBound, self.upperBound = arguments

    def differentiate(self, VarName):
        raise Exception("Cannot differentiate a bounded anti-derivative")

    def toTex(self, needsBrackets=False, environment=False):
        return "\\left["+self.arguments[0].toTex()+"\\right]_{ "+self.arguments[2].toTex()+" }^{ "+self.arguments[3].toTex()+" }"
