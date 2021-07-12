from .unification import Unification
class Step:
    def __init__(self, expressionBefore, expressionAfter, rule=False, unification=Unification()):
        self.expressionBefore = expressionBefore
        self.expressionAfter = expressionAfter
        self.rule = rule

    def isTrivial(self):
        return self.rule and self.rule.isTrivial()

    def toTex(self, needsBrackets=False, environment=False):
        return self.expressionAfter.toTex(False, environment)

    def ruleTex(self):
        return self.rule.toTex()

    def ruleApplied(self):
        return True

    def getResult(self):
        return self.expressionAfter

class EmptyStep(Step):
    def __init__(self, expressionBefore):
        self.expressionBefore = expressionBefore

    def ruleApplied(self):
        return False

    def getResult(self):
        return self.expressionBefore

    def toTex(self):
        return "No step"

    def ruleTex(self):
        return "No step"

    def isTrivial(self):
        return True


class Workings:
    def __init__(self, steps=[]):
        self.steps = steps
        #Store the most recent result as the result of the workings(final step)
        if(len(steps) > 0):
            self.result = self.steps[len(self.steps)-1].getResult()

    def getSteps(self):
        return self.steps

    def getResult(self):
        return self.result
    
    def getResultTex(self, needsBrackets=False, environment=False):
        return self.getResult().toTex(needsBrackets, environment)

    def getProblem(self):
        return self.steps[0].expressionBefore

    def setResult(self, result):
        self.result = result

    def withStep(self, step):
        return Workings(self.steps+[step])

#This is a class to store steps that do not have objects of expression class stored to show transformations
class TextStep(Step):
    def __init__(self, text, ruleTex=False):
        self.text = text
        self.rule = ruleTex

    def toTex(self, needsBrackets=False, environment=False):
        if(environment):
            return "\\begin{"+environment+"}"+self.text+"\\end{"+environment+"}"
        print(environment)
        return self.text

    def getResult(self):
        return self
        
    def isTrivial(self):
        False

    def ruleTex(self):
        return self.rule
