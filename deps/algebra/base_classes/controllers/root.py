from .controller import Controller


class RootController(Controller):
    name = 'Root'

    def __init__(self, arguments):
        super().__init__(arguments)
        self.function, self.power = arguments

    def evaluate(self):
        return self.function.evaluate()**(1/(self.power.evaluate()))

    def differentiate(self, VarName):
        return (self.power.differentiate(VarName)*self.power**((1-self.function)/self.function))/self.function

    def toTex(self, needsBrackets=False, environment=False):
        if self.power.evaluate() == 2:
            return "\sqrt{ "+self.function.toTex()+" }"
        else:
            return "\sqrt[^{ "+self.power.toTex()+" }]{ "+self.function.toTex()+" }"

    def canCalculate(self):
        return False
