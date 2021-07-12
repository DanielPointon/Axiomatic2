from .FunctionalRule import *
from ..base_classes.base import *
from .RuleVariable import RuleVar, TypedRuleVar
from ..base_classes.base import NumberController
from ..base_classes.controllers.addition import AdditionController
from .collectionUtils import *
from ..base_classes.set import Set


def simplifyExpression(expression, substitution):
    multiplier_terms=Set()
    for argument in expression.getArguments():
        splitFractionResult=splitFraction(argument)
        if splitFractionResult:
            numerator,denominator=splitFractionResult
            if denominator.getType()=="Multiplication":
                for term in denominator.getArguments():
                    multiplier_terms.add(term)
            else:
                multiplier_terms.add(denominator)
    if(not multiplier_terms):
        return False
    sum_terms=[]
    for argument in expression.getArguments():
        splitFractionResult=splitFraction(argument)
        if splitFractionResult:
            numerator, denominator=splitFractionResult
            if denominator.getType()=="Multiplication":
                current_terms=Set(denominator.getArguments())
                extra_multipliers=multiplier_terms.difference(current_terms)
            else:
                extra_multipliers=multiplier_terms.difference(Set([denominator]))
            if(not extra_multipliers):
                sum_terms.append(numerator)
            else:
                sum_terms.append(numerator*CommutativeExpression(MultiplicationController, extra_multipliers.toList()))
        else:
            sum_terms.append(argument*CommutativeExpression(MultiplicationController, multiplier_terms.toList()))
    return Expression(AdditionController, sum_terms)/CommutativeExpression(MultiplicationController,multiplier_terms.toList())
CombiningFractionsRule=FunctionalRule(TypedRuleVar("Addition"), [] , simplifyExpression, "fraction combining by cross-multiplication")
