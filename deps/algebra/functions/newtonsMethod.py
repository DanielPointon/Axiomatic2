from ..base_classes.simplification import TextStep, Workings, Step
from ..functions.simplify import simplify
from ..equation import Equation
from ..base_classes.base import Num
from ..rules import TrivialRules


def NewtonRaphson(x, target_var, function, derivative):
    return Num(x.evaluate()-(function.substitute(target_var, x).evaluate())/(derivative.substitute(target_var, x).evaluate()))


ruleLatex = 'x_{n+1}=x_{n}-\\frac{f(x_{n})}{f\'(x)}'
iterationThreshold = 100


def getNewtonsWorkings(equation, targetVariable):
    workings = Workings()
    leftHandSide, rightHandSide = equation.getArguments()
    initialProblem = simplify(
        Equation(leftHandSide-rightHandSide, Num(0)), TrivialRules).getResult()
    workings = workings.withStep(Step(equation, initialProblem))
    function = initialProblem.getArguments()[0]
    derivative = simplify(function.differentiate(targetVariable),
                          TrivialRules).getResult()

    xN = Num(1.5)
    for i in range(iterationThreshold):
        xN = NewtonRaphson(xN, targetVariable, function, derivative)
        workings = workings.withStep(
            TextStep("x_{"+str(i)+"}="+xN.toTex(), ruleLatex))
    return workings
