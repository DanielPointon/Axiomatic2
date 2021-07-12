from .controller import Controller


class VariableController(Controller):
    name = 'Variable'

    def __init__(self, name=False):
        self.name = name

    def toTex(self, needsBrackets=False, environment=False):
        return self.name if self.name else "p"

    def substituteMany(self, substitutions):
        if self.name in substitutions:
            return substitutions[self.name]
        else:
            return self

    def getName(self):
        return self.name

    def differentiate(self, VarName):
        return 1