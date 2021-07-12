from .controller import Controller


class PlusMinusController(Controller):
    name = 'PlusMinus'

    def __init__(self, arguments):
        super().__init__(arguments)

    def evaluate(self):
        raise Exception("Cannot Calculate +-")

    def differentiate(self, VarName):
        raise Exception("Cannot differentiate +-")

    def toTex(self, needsBrackets=False, environment=False):
        return "\pm "+self.arguments[0].toTex()

    def canCalculate(self):
        return False
