from .controller import Controller


class DivisionController(Controller):
    name = 'Division'

    def __init__(self, arguments):
        super().__init__(arguments)
        self.numerator, self.denominator = arguments

    def evaluate(self):
        return self.numerator.evaluate()/self.denominator.evaluate()

    def differentiate(self, VarName):
        returnNumerator = self.denominator * \
            self.numerator.differentiate(VarName)-self.numerator * \
            self.denominator.differentiate(VarName)
        returnDenominator = self.denominator**2
        return returnNumerator/returnDenominator

    def toTex(self, needsBrackets=False, environment=False):
        return '\\frac{ '+self.numerator.toTex()+' }{ '+self.denominator.toTex()+' }'
