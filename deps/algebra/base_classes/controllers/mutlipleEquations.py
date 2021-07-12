from .controller import Controller


class MultipleEquationsController(Controller):
    name = 'MultipleEquations'
    customEnvironmentStatus = True

    def toTex(self, needsBrackets=False, environment=False):
        if(environment):
            return ''.join([arg.toTex(False, environment) for arg in self.arguments])
        else:
            return (', \\newline ').join([arg.toTex(False, environment) for arg in self.arguments])

    def canCalculate(self):
        return False
