from .FunctionalRule import *
from ..base_classes.base import *
from .RuleVariable import TypedRuleVar
from ..base_classes.base import NumberController
from ..base_classes.controllers.boundedAntiderivative import BoundedAntiDerivativeController
from .collectionUtils import *

def simplifyExpression(antiDerivative, substitution):
    expression, variable, lowerBound, upperBound = antiDerivative.getArguments()
    if expression.getType() == "IndefiniteIntegral":
        return False
    else:
        return expression.substitute(variable, upperBound)-expression.substitute(variable, lowerBound)


antiDerivativeRule = FunctionalRule(
    TypedRuleVar("BoundedAntiDerivative"), [], simplifyExpression, "evaluation of anti-derivative")
