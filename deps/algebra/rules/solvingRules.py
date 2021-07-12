from .BasicRule import *
from .FunctionalRule import *
from ..rules.RuleVariable import NotFunctionOf,FunctionOf
from ..rules.trivialRules import getRules
from ..equation import Equation
from ..base_classes.base import *
from ..utils import ArcSin, ArcCos, ArcTan, Sin, Cos, Tan, sqrt, plusMinus, pi, Exp, Ln
from ..base_classes.controllers.root import RootController
from ..base_classes.controllers.plusminus import PlusMinusController
from ..base_classes.controllers.mutlipleEquations import MultipleEquationsController
from ..base_classes.controllers.pi import PiController
from .functionCollection import getRule
    
n=Var('n')
#These are the solving rules, the majority of these could in fact be read from a text file. The problem with this is that it would 
#Require the parser to be applied to dozens of rules which would be very slow when the program boots up, as a result they are defined in this form

def getSolvingRules(variable):
    #fx is used to denote a function of x, the name is the same as the mathematical definition without brackets, same goes for gx
    fx=FunctionOf("f",variable)
    gx=FunctionOf("g",variable)
    #These have no meaning beyond being a mathematical expression, hence letter variable names
    h=NotFunctionOf("a",variable)
    i=NotFunctionOf("b",variable)
    j=NotFunctionOf("c",variable)
    #These rules are all patterns, which our program attempts to match to a given expression. 
    equationRules=[
        BasicRule(Equation(h*(fx**2)+i*fx, j), Equation(fx, (-1*i+plusMinus(sqrt(i**2-4*h*(-1*j))))/(2*h))),
        BasicRule(Equation(fx**2, i), Equation(fx, plusMinus(Expression(RootController, [i, Num(2)])))),
        BasicRule(Equation(fx/gx, i), Equation(fx, gx*i)),
        BasicRule(Equation(fx/h, i), Equation(fx, h*i)),
        BasicRule(Equation(fx+h, i), Equation(fx, i-h)),
        BasicRule(Equation(fx, gx+h), Equation(fx-gx, h)),
        BasicRule(Equation(fx-h, i), Equation(fx, i+h)),
        BasicRule(Equation(Exp(fx), h), Equation(fx, Ln(h))),
        BasicRule(Equation(fx**h, i), Equation(fx, Expression(RootController, [i, h]))),
        BasicRule(Equation(fx*h, i), Equation(fx, i/h)),
        BasicRule(Equation(h/fx, i), Equation(h/i, fx)),
        BasicRule(Equation(Ln(fx), h), Equation(fx, Exp(h))),
        BasicRule(Equation(Sin(fx), h), Expression(MultipleEquationsController, [Equation(fx, ArcSin(h)+2*pi*n) , Equation(fx, ArcSin(-1*h)+(2*n+1)*pi) ])),
        BasicRule(Equation(Cos(fx), h), Expression(MultipleEquationsController, [Equation(fx, ArcCos(h)+2*pi*n) , Equation(fx, -1*ArcCos(h)+2*n*pi) ])),
        BasicRule(Equation(Tan(fx), h), Equation(fx, ArcTan(h)+pi*n)),
        BasicRule(Equation(fx**2+h*fx, i), Equation(((fx+h/Num(2))**2-(h**2)/Num(4)), i)),
        BasicRule(Equation(fx**2+fx, i), Equation(((fx+1/Num(2))**2-(1)/Num(4)), i)),
        # BasicRule(Equation(fx+gx,Num(0)),Equation(fx/(-1*gx),Num(1))),
        BasicRule(Equation(fx,gx),Equation(fx-(gx),Num(0))),
        BasicRule(Equation(Sin(fx)/(h*Cos(fx)), i),Equation(Sin(fx)/Cos(fx),h*i)),
        BasicRule(Equation((h*Sin(fx))/(Cos(fx)), i),Equation(Sin(fx)/Cos(fx),i/h)),
        BasicRule(Equation(fx*gx, Num(0)),Expression(MultipleEquationsController, [Equation(fx,Num(0)), Equation(gx,Num(0))])),
        BasicRule(Equation(fx**gx,Num(0)), Equation(fx, Num(0))),
        BasicRule(Equation(fx**gx,Num(1)), Expression(MultipleEquationsController, [Equation(gx, Num(0)),Equation(fx, Num(1))])),
        BasicRule(Equation(h*Sin(fx)+i*Cos(fx), Num(0)), Equation(Tan(fx), (-1*i)/h )),
        BasicRule(Equation(Sin(fx)+i*Cos(fx), Num(0)), Equation(Tan(fx), (-1*i) )),
        BasicRule(Equation(Sin(fx)+Cos(fx), Num(0)), Equation(Tan(fx), (-1) )),
        BasicRule(Equation(h*Sin(fx)+Cos(fx), Num(0)), Equation(Tan(fx), (-1)/h )),
        getRule(variable),
    ]   
    return equationRules+getRules(variable)
