from .FunctionalRule import *
from ..base_classes.base import *
from .RuleVariable import RuleVar
from .RuleVariable import TypedRuleVar
from ..base_classes.base import NumberController
from ..base_classes.controllers.addition import AdditionController
from ..base_classes.controllers.multiplication import MultiplicationController
from ..base_classes.controllers.derivative import DerivativeController
from .collectionUtils import *

def simplifyExpression(antiDerivative, substitution):
    variable, expression = antiDerivative.getArguments()
    if not expression.getType() == "Variable":
        return expression.differentiate(variable)
    else:
        return False


derivativeEvaluationRule = FunctionalRule(
    TypedRuleVar("Derivative"), [], simplifyExpression, "evaluation of derivative")
