from .controller import Controller


class NumberController(Controller):
    name = 'Number'

    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value

    def differentiate(self, VarName):
        return 0

    def toTex(self, needsBrackets=False, environment=False):
        if(int(self.value) == self.value and type(self.value) == float):
            return str(int(self.value))
        else:
            return str(round(self.value,3))