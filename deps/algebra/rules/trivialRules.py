from .BasicRule import *
from ..base_classes.base import *
from .RuleVariable import RuleVar,TypedRuleVar, NotFunctionOf
# from .collectVars import varCollectionRule
from .collectVarsMultiplication import productCollectionRule
from ..base_classes.controllers.addition import AdditionController
from ..base_classes.controllers.number import NumberController
from ..base_classes.controllers.multiplication import MultiplicationController
from .integerCollection import additionEvaluationRule, multiplicationEvaluationRule
from .cancellationFractions import fractionCancellationRule
from .additionFractionCollection import CombiningFractionsRule
from .RuleVariable import CalculateableRuleVar
from .roundIntegers import roundingIntegersRule
from .complexRoots import factorOutComplexRule
from ..base_classes.controllers.root import RootController
from .integralRules import integralRules
from .evaluateDerivatives import derivativeEvaluationRule
from ..utils import ArcSin, ArcCos, ArcTan, Sin, Cos, Tan, Sec, pi, sqrt, Exp, Ln
from .termCollection import getRule
x=RuleVar('x')
y=RuleVar('y')
p=RuleVar('p')
q=RuleVar('q')
evaluateableExpressionOne=CalculateableRuleVar()
evaluateableExpressionTwo=CalculateableRuleVar()
#Addition TypedRule variables(represents a sum of expressions)
a=TypedRuleVar("Addition")
b=TypedRuleVar("Addition")
#Multiplication TypedRule variables(represents a product of expressions)
c=TypedRuleVar("Multiplication")
d=TypedRuleVar("Multiplication")
NumPlaceholder=TypedRuleVar("Number")

#This will match all expressions, it should be used in addition/multiplication as it removes the biggest term possible when simplifying
matchAll=NotFunctionOf('h(x)', Var())

#These are the solving rules, the majority of these could in fact be read from a text file. The problem with this is that it would 
#Require the parser to be applied to dozens of rules which would be very slow when the program boots up, as a result they are defined in this form


def getRules(variable):
    return [
        BasicRule(x/(p*sqrt(y)), (x*sqrt(y))/(p*y)),
        BasicRule(x/x, Num(1)),
        BasicRule((x*y)**p, (x**p)*(y**p)),
        BasicRule(x*Num(0), Num(0),trivial=True),
        BasicRule(matchAll+Num(0), matchAll,trivial=True),
        BasicRule(Exp(Ln(x)), x),
        BasicRule(Num(1)/Num(1),Num(1),trivial=True),
        BasicRule((x**2)**2, x**Num(2*2)),
        BasicRule(x**0, Num(1),trivial=True),
        BasicRule(x**1, x,trivial=True),
        BasicRule(Ln(x)*y, Ln(x**y), trivial=True),
        BasicRule(x*1, x,trivial=True),
        BasicRule(Num(1)**x, Num(1), trivial=True),
        BasicRule(Num(0)-x, Num(-1)*x, trivial=True),
        #Collecting variables during addition
        BasicRule(Expression(AdditionController, [x]), x, True),
        BasicRule(Expression(AdditionController, [a,b]),CommutativeExpression(AdditionController, [a.getArguments(), b.getArguments()]),trivial=True),
        BasicRule(Expression(AdditionController, [b,a]),CommutativeExpression(AdditionController, [b.getArguments(), a.getArguments()]),trivial=True),
        BasicRule(Expression(AdditionController, [a,x]),CommutativeExpression(AdditionController, [a.getArguments(), x]),trivial=True),
        BasicRule(Expression(AdditionController, [x,a]),CommutativeExpression(AdditionController, [x, a.getArguments()]),trivial=True),
        BasicRule(Expression(AdditionController, [a, x]),CommutativeExpression(AdditionController, [a.getArguments(), x]),trivial=True),
        BasicRule(Expression(AdditionController, [x, a]),CommutativeExpression(AdditionController, [x, a.getArguments()]),trivial=True),
        #Collecting arguments during mutliplication
        BasicRule(c*d,CommutativeExpression(MultiplicationController, [c.getArguments(), d.getArguments()]),trivial=True),
        BasicRule(c*x,CommutativeExpression(MultiplicationController, [c.getArguments(), x]),trivial=True),
        BasicRule(c*x,CommutativeExpression(MultiplicationController, [c.getArguments(), x]),trivial=True),
        BasicRule((x**y)**q, x**(y*q),trivial=True),
        BasicRule(Num(0)/x,Num(0),trivial=True),
        BasicRule(Sin(x)/Cos(x), Tan(x)),
        BasicRule(Num(0)**x, Num(0)),
        BasicRule((x/y)**p, (x**p)/(y**p)),
        BasicRule(Num(0)**Var('x'), Num(0), trivial=True),
        BasicRule(Expression(MultiplicationController, [x]), x, trivial=True),
        BasicRule(x-y, x+Num(-1)*y, trivial=True),
        BasicRule(Expression(RootController, [Num(0), x]), Num(0)),
        BasicRule(Expression(RootController, [Num(1), x]), Num(1)),
        #Inverse trig evaluation
        BasicRule(ArcSin(Num(0)), Num(0)),
        BasicRule(ArcSin(Num(1)), pi/Num(2)),
        BasicRule(ArcSin(sqrt(2)/Num(2)),pi/Num(4)),
        BasicRule(ArcSin(sqrt(3)/Num(2)), pi/Num(3)),
        BasicRule(ArcSin(Num(-1)), -1*pi/Num(2)),
        BasicRule(ArcSin(-1*sqrt(2)/Num(2)),-1*pi/Num(4)),
        BasicRule(ArcSin(-1*sqrt(3)/Num(2)), -1*pi/Num(3)),
        #All the custom rules that cant be expressed as RHS=LHS 
        CombiningFractionsRule,
        additionEvaluationRule,
        fractionCancellationRule,
        multiplicationEvaluationRule,
        productCollectionRule,
        roundingIntegersRule,
        factorOutComplexRule,
        getRule(variable),
        derivativeEvaluationRule,
        #If we have an evaluatable sub-part, evaluate it!
        BasicRule(evaluateableExpressionOne, evaluateableExpressionOne.evaluate(), trivial=True),
        BasicRule(Sin(x)+Cos(x), Sin(2*x)),
        getRule(variable)
    ]+integralRules

TrivialRules=getRules(False)