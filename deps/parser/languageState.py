from deps.algebra.base_classes.unification import Unification
from deps.algebra.base_classes.simplification import *


class LanguageState:
    def __init__(self):
        self.variables = {}
        self.methods = {}
        self.output = Workings()

    def addVariable(self, variableName, value):
        self.variables[variableName] = value

    def addMethod(self, methodName, method):
        self.methods[methodName.getName()] = method

    def addStep(self, term):
        if(len(self.output.getSteps()) == 0):
            self.output = self.output.withStep(EmptyStep(term))
        else:
            self.output = self.output.withStep(
                Step(self.output.getResult(), term))

    def evaluateExpression(self, expression):
        return expression.substituteMany(Unification(self.variables))

    def getMethod(self, methodName):
        return self.methods[methodName.getName()]