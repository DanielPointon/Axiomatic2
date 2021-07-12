from .FunctionalRule import *
from ..base_classes.base import Expression
from .RuleVariable import RuleVar, FunctionOf, NotFunctionOf
from .RuleVariable import TypedRuleVar
from ..base_classes.base import NumberController
from ..base_classes.controllers.addition import AdditionController
from ..base_classes.controllers.division import DivisionController
from .collectionUtils import *
from ..base_classes.set import Set
import copy

def getRule(variable):
    def simplifyExpression(expression, substitution):
        termCollection={}
        extra=[]
        changeMade=False
        for term in expression.getArguments():
            if not (variable and FunctionOf('f(x)', variable).unify(term)):
                notFunctionPlaceholder=NotFunctionOf('h(x)', Var())
                numberPlaceholder=TypedRuleVar("Number")
                unification=(notFunctionPlaceholder*numberPlaceholder).unify(term)
                if unification:
                    unification=(notFunctionPlaceholder*numberPlaceholder).unify(term)
                    notFunction=unification.getVar(notFunctionPlaceholder)
                    number=unification.getVar(numberPlaceholder)
                    termCollection, tempChangeMade= insertIntoTable(termCollection, notFunction, number)
                    if tempChangeMade:
                        changeMade=True
                else:
                    termCollection, tempChangeMade= insertIntoTable(termCollection, term, Num(1))
                    if tempChangeMade:
                        changeMade=True
            else:
                extra.append(term)
        termList=convertHashTableToList(termCollection, lambda term: term['expression']* term['count'])
        if changeMade:
            return Expression(AdditionController,termList)+Expression(AdditionController,extra)
        else:
            return False
    return FunctionalRule(TypedRuleVar("Addition"), [] , simplifyExpression, "collection of like terms")
