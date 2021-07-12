from .FunctionalRule import *
from ..base_classes.base import *
from .RuleVariable import FunctionOf, NotFunctionOf
from .RuleVariable import TypedRuleVar
from ..base_classes.controllers.addition import AdditionController
from .collectionUtils import *


def getRule(variable):
    def simplifyExpression(expression, substitution):
        extra = []
        summationTerms = {}
        changeMade = False
        fOfxPlaceholder = FunctionOf('f(x)', variable)
        hOfxPlaceholder = NotFunctionOf('h(x)', variable)
        for term in expression.getArguments():
            unification = (fOfxPlaceholder*hOfxPlaceholder).unify(term)
            if unification:
                fOfx = unification.getVar(fOfxPlaceholder)
                hOfx = unification.getVar(hOfxPlaceholder)
                summationTerms, tempChangeMade = insertIntoTable(
                    summationTerms, fOfx, hOfx)
                if tempChangeMade:
                    changeMade = True
            else:
                if fOfxPlaceholder.unify(term):
                    summationTerms, tempChangeMade = insertIntoTable(
                        summationTerms, term, Num(1))
                    if tempChangeMade:
                        changeMade = True
                else:
                    extra.append(term)
        if changeMade:
            summationTermsAsList = [summationTerms[term]['expression']
                                    * summationTerms[term]['count'] for term in summationTerms]
            return Expression(AdditionController, summationTermsAsList+extra)
        else:
            return False
    return FunctionalRule(TypedRuleVar("Addition"), [], simplifyExpression, "collection of like terms")
