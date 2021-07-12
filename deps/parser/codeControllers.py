from deps.algebra.base_classes.base import Num
from deps.algebra.functions.simplify import simplify
from deps.algebra.rules.trivialRules import TrivialRules


# These controllers are used to represent a terminal operation
# Execute function takes a state variable and mutate it according to the lines of code 
# the user is trying to execute

class CodeController:
    def __init__(self, childNodes):
        self.childNodes = childNodes

    def getName(self):
        return self.name


class ForLoopController(CodeController):
    name = "ForLoop"

    def __init__(self, childNodes):
        self.initialLine, self.conditionForReloop, self.increment, self.codeBlock = childNodes

    def execute(self, state):
        state = self.initialLine.execute(state)
        while state.evaluateExpression(self.conditionForReloop).evaluate():
            state = self.codeBlock.execute(state)
            state = self.increment.execute(state)
        return state


class CodeBlockController(CodeController):
    name = "CodeBlock"

    def __init__(self, childNodes):
        self.childNodes = childNodes

    def execute(self, state):
        for childNode in self.childNodes:
            state = childNode.execute(state)
        return state


class LineOfCodeController(CodeController):
    name = "LineOfCode"

    def __init__(self, childNodes):
        self.expression = childNodes[0]

    def execute(self, state):
        if self.expression.getType() == "Equation":
            leftHandSide, rightHandSide = self.expression.getArguments()
            if leftHandSide.getType() == "Variable":
                simplifiedrightHandSide = simplify(state.evaluateExpression(rightHandSide), TrivialRules).getResult()
                state.addVariable(leftHandSide. getName(),
                                  simplifiedrightHandSide)
        return state


class MethodDefinitionController(CodeController):
    name = "MethodDefinition"

    def __init__(self, childNodes):
        self.functionName, self.variableName, self.codeBlock = childNodes

    def execute(self, state):
        state.addMethod(self.functionName, self)
        return state

    def getVariable(self):
        return self.variableName


class IfStatementController(CodeController):
    name = "IfStatement"

    def __init__(self, childNodes):
        self.condition, self.codeBlock = childNodes

    def execute(self, state):
        if(state.evaluateExpression(self.condition).evaluate()):
            return self.codeBlock.execute(state)
        else:
            return state


class OutputController(CodeController):
    name = "Output"

    def __init__(self, childNodes):
        self.expressionToOutput = childNodes[0]

    def execute(self, state):
        subbedInVersion = state.evaluateExpression(self.expressionToOutput)
        if subbedInVersion.canCalculate():
            state.addStep(Num(subbedInVersion.evaluate()))
        else:
            state.addStep(simplify(subbedInVersion, TrivialRules).getResult())
        return state


class OutputRawController(CodeController):
    name = "OutputRaw"

    def __init__(self, childNodes):
        self.expressionToOutput = childNodes[0]

    def execute(self, state):
        subbedInVersion = state.evaluateExpression(self.expressionToOutput)
        state.addStep(subbedInVersion)
        return state

#This is the base class for any line/block of code, plays the same role as the expression
#class does for mathematical values(storing controller and using it to execute lines of code)
class CodeConstruct:
    def __init__(self, childNodes=False, controller_type=False):
        self.childNodes = childNodes
        self.controller_type = controller_type
        self.controller = controller_type(childNodes)

    def matches(self, expression):
        return type(expression) == CodeConstruct

    def execute(self, state):
        return self.controller.execute(state)

    def getType(self):
        return self.controller.name

    def __str__(self):
        return "CodeConstruct"


class LessThanController(CodeController):
    name = "LessThan"

    def evaluate(self):
        return self.childNodes[0].evaluate() < self.childNodes[1].evaluate()

    def canCalculate(self):
        return self.leftHandSide.canEvaluate() and self.rightHandSide.canEvaluate()

    def toTex(self, needsBrackets=False):
        return self.childNodes[0].toTex()+'<'+self.childNodes[1].toTex()


class GreaterThanController(CodeController):
    name = "GreaterThan"

    def __init__(self, childNodes):
        self.childNodes = childNodes

    def evaluate(self):
        return self.childNodes[0].evaluate() > self.childNodes[1].evaluate()

    def canCalculate(self):
        return self.leftHandSide.canEvaluate() and self.rightHandSide.canEvaluate()

    def toTex(self, needsBrackets=False):
        return self.leftHandSide.toTex()+'>'+self.rightHandSide.toTex()


class CallMethodController(CodeController):
    name = "CallMethod"

    def __init__(self, childNodes):
        self.expressionToOutput, self.variable = childNodes

    def execute(self, state):
        variable = state.getMethod()
        subbedInVersion = state.evaluateExpression(self.expressionToOutput)
        state.addStep(simplify(subbedInVersion, TrivialRules).getResult())
        return state
