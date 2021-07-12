from .BasicRule import *
from ..utils import Sin,Tan, Cos, ArcTan, ArcCos, ArcSin, Exp, Ln
from ..base_classes.controllers.mutlipleEquations import MultipleEquationsController
from ..base_classes.controllers.indefiniteIntegral import IndefiniteIntegralController
from ..base_classes.controllers.definiteIntegral import DefiniteIntegralController
from ..base_classes.controllers.boundedAntiderivative import BoundedAntiDerivativeController
from .boundedAntiDerivativeEvaluation import antiDerivativeRule
from .RuleVariable import NotFunctionOf
from .RuleVariable import TypedRuleVar
#These variables are named as such because they have no meaning beyond representing a mathematical expression
x=RuleVar('x')
y=RuleVar('y')
p=RuleVar('p')
q=RuleVar('q')
c=Var(name='c')
scalar=TypedRuleVar("Number", "s")
#This will match any term, and will expand to capture sums and products
expansiveMatcher=NotFunctionOf('p', Var())
integralRules=[
    #Cases where y=1
    BasicRule(Expression(IndefiniteIntegralController, [Sin(expansiveMatcher), expansiveMatcher]), -1*Cos(expansiveMatcher)),
    BasicRule(Expression(IndefiniteIntegralController, [Cos(expansiveMatcher),expansiveMatcher]), Sin(expansiveMatcher)),
    BasicRule(Expression(IndefiniteIntegralController, [Tan(expansiveMatcher), expansiveMatcher]), Ln(Cos(expansiveMatcher))),
    BasicRule(Expression(IndefiniteIntegralController, [Exp(expansiveMatcher), expansiveMatcher]), Exp(expansiveMatcher)),
    BasicRule(Expression(IndefiniteIntegralController, [expansiveMatcher, expansiveMatcher]), 1/Num(2)*expansiveMatcher**Num(2)),
    BasicRule(Expression(IndefiniteIntegralController, [scalar, expansiveMatcher]), scalar*expansiveMatcher),
    #Cases where y=/=1
    BasicRule(Expression(IndefiniteIntegralController, [Sin(y*x), x]), -1/y*Cos(y*x)),
    BasicRule(Expression(IndefiniteIntegralController, [x**y, x]), 1/(y+1)*x**(y+1)),
    BasicRule(Expression(IndefiniteIntegralController, [Cos(y*x),x]), 1/y*Sin(y*x)),
    BasicRule(Expression(IndefiniteIntegralController, [Tan(y*x), x]), -1/y*Ln(Cos(y*x))),
    BasicRule(Expression(IndefiniteIntegralController, [Exp(y*x), x]), 1/y*Exp(y*x)),
    #General integration rules
    BasicRule(Expression(IndefiniteIntegralController, [scalar*x, y]), scalar*Expression(IndefiniteIntegralController, [x, y])),
    BasicRule(Expression(IndefiniteIntegralController, [expansiveMatcher+q, x]), Expression(IndefiniteIntegralController, [expansiveMatcher, x])+Expression(IndefiniteIntegralController, [q, x])),
    BasicRule(Expression(DefiniteIntegralController, [x, y, p, q]), Expression(BoundedAntiDerivativeController, [Expression(IndefiniteIntegralController, [p, q]), q, x, y])),
    BasicRule(Expression(DefiniteIntegralController, [x, y, p, q]), Expression(BoundedAntiDerivativeController, [Expression(IndefiniteIntegralController, [p, q]), q, x, y])),
    antiDerivativeRule
]