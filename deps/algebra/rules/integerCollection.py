from .FunctionalRule import *
from ..base_classes.base import *
from .RuleVariable import RuleVar
from .RuleVariable import TypedRuleVar
from ..base_classes.base import AdditionController
from ..base_classes.controllers.number import NumberController
from functools import reduce


def simplifyExpression(expression, substitution):
    if expression.getType() == "Addition":
        def reducer(a, b): return a+b
        initialValue = 0
    elif expression.getType() == "Multiplication":
        def reducer(a, b): return a*b
        initialValue = 1
    controllerType = expression.getControllerType()
    arguments = expression.getArguments()
    result = initialValue
    non_integer_arguments = []
    for argument in arguments:
        # Begin seperating integers and non integers
        if(type(argument) == Num):
            result = reducer(result, argument.evaluate())
        else:
            non_integer_arguments.append(argument)
    new_arguments = non_integer_arguments+[Num(result)]

    # Unpack empty addition/multiplication
    if(len(arguments) == 1):
        return arguments[0]

    if(len(new_arguments) < len(arguments)):
        return Expression(controllerType, new_arguments)
    else:
        return False


additionEvaluationRule = FunctionalRule(
    TypedRuleVar("Addition"), [], simplifyExpression, "addition of real numbers", True)

multiplicationEvaluationRule = FunctionalRule(
    TypedRuleVar("Multiplication"), [], simplifyExpression, "multiplication of real numbers")
