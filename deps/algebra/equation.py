from .base_classes.simplification import TextStep, Workings
from .rules.trivialRules import TrivialRules
from .base_classes.base import Num, CommutativeExpression
from .base_classes.controllers.equation import EquationController
from .base_classes.unification import Unification

# This is a class used to represent an equation
# It exists primarily for future development, but also to allow equation rules to be written
# commutatively(whether a term is on the left or right hand side doesn't matter)
# As it extends the CommutativeExpression class


class Equation(CommutativeExpression):
    def __init__(self, leftHandSide, rightHandSide, workings=Workings()):
        self.leftHandSide = leftHandSide
        self.rightHandSide = rightHandSide
        self.arguments = [leftHandSide, rightHandSide]
        self.workings = workings
        self.controller_type = EquationController
        self.controller = self.controller_type(self.arguments)

    def getleftHandSide(self):
        return self.leftHandSide

    def getrightHandSide(self):
        return self.rightHandSide

    def mutate(self, newState):
        if self.firstLine():
            newState = newState.withStep(TextStep(self.toTex()))
        return newState.withStep(TextStep(newState.toTex()))

    def substitute(self, targetVar, value):
        newState = Equation(self.leftHandSide.substitute(
            targetVar, value), self.rightHandSide.substitute(targetVar, value))
        return self.mutate(newState)

    def withStep(self, step):
        return Equation(self.leftHandSide, self.rightHandSide, self.workings.withStep(step))

    def __add__(self, term):
        newState = Equation(self.leftHandSide+term, self.rightHandSide +
                            term, self.workings).simplify()
        return self.mutate(newState)

    def __mul__(self, term):
        newState = Equation(self.leftHandSide*term, self.rightHandSide *
                            term, self.workings).simplify()
        return self.mutate(newState)

    def __sub__(self, term):
        newState = Equation(self.leftHandSide-term, self.rightHandSide -
                            term, self.workings).simplify()
        return self.mutate(newState)

    def __truediv__(self, term):
        newState = Equation(self.leftHandSide/term, self.rightHandSide /
                            term, self.workings).simplify()
        return self.mutate(newState)
    # Simplify both sides of equation

    def simplify(self):
        return self

    def calculaterightHandSide(self):
        newState = Equation(self.leftHandSide, Num(
            self.rightHandSide.evaluate()), self.workings).simplify()
        return self.mutate(newState)

    def firstLine(self):
        return len(self.workings.getSteps()) == 0

    def substituteMany(self, unification):
        return Equation(self.leftHandSide.substituteMany(unification), self.rightHandSide.substituteMany(unification))
    # Unify defined recursively

    def unify(self, other, index=0, usedIndexes=None):
        if usedIndexes is None:
            usedIndexes = []
        # In the base case in which there are no terms left to unify
        if(self.getArity() == len(usedIndexes)):
            return Unification()
        if(not self.getArity() == other.getArity()):
            return False
        if self.getType() == other.getType():
            currentSelfTerm = self.getArguments()[index]
            otherArguments = other.getArguments()
            for i in range(len(otherArguments)):
                # Check the index has not already been used
                if not i in usedIndexes:
                    termUnification = currentSelfTerm.unify(otherArguments[i])
                    if(termUnification):
                        #Substituting in avoids variables having multiple values
                        selfWithSub = self.substituteMany(termUnification)
                        fullUnification = selfWithSub.unify(
                            other, index+1, usedIndexes+[i])
                        if fullUnification:
                            return termUnification.merge(fullUnification)
        return False
