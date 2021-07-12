from .FunctionalRule import *
from ..base_classes.base import *
from .RuleVariable import RuleVar
from .RuleVariable import TypedRuleVar
from ..base_classes.base import NumberController
from ..base_classes.controllers.addition import AdditionController
from ..base_classes.controllers.multiplication import MultiplicationController
from .collectionUtils import *

def simplifyExpression(expression, substitution):
    value = expression.evaluate()
    valueAsInt = int(value)
    if(valueAsInt == value and type(value) == float):
        return Num(valueAsInt)
    else:
        return False


roundingIntegersRule = FunctionalRule(
    TypedRuleVar("Number"), [], simplifyExpression, "rounding", True)
