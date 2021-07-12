from .FunctionalRule import *
from ..base_classes.base import *
from .RuleVariable import RuleVar
from .RuleVariable import TypedRuleVar
from ..base_classes.base import NumberController
from ..base_classes.controllers.addition import AdditionController
from ..base_classes.controllers.multiplication import MultiplicationController
from .collectionUtils import *
from ..base_classes.controllers.root import RootController
from ..base_classes.controllers.complex import ComplexUnitController

def factorOutComplexUnits(expression, substitution):
    thingBeingRooted, power = expression.getArguments()
    if(power.evaluate() == 2):
        if type(thingBeingRooted) == Num:
            if thingBeingRooted.evaluate() < 0:
                newThingToRoot = Num(abs(thingBeingRooted.evaluate()))
                return Expression(RootController, [newThingToRoot, power])*Expression(ComplexUnitController, [])


factorOutComplexRule = FunctionalRule(
    TypedRuleVar("Root"), [], factorOutComplexUnits, "$\sqrt{-1}=i$")
