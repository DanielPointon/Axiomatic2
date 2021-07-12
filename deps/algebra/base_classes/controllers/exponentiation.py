from .controller import Controller


class ExponentiationController(Controller):
    name = 'Exponentiation'

    def __init__(self, arguments):
        super().__init__(arguments)
        self.base, self.power = arguments

    def toTex(self, needsBrackets=False, environment=False):
        if self.base.isSingleTerm():
            # No need to put brackets around a term if it's just x, \sin(x), etc
            baseTex = self.base.toTex()
        else:
            baseTex = "("+self.base.toTex()+")"
        return '{ '+baseTex+' }'+'^{ '+self.power.toTex(needsBrackets=True)+' }'

    def evaluate(self):
        return self.base.evaluate()**self.power.evaluate()

    def differentiate(self, VarName):
        return ((self.base.ln())*self.power).exp().differentiate(VarName)
