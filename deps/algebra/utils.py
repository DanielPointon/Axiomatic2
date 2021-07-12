
from .base_classes.controllers.cosInverse import ArcCosController
from .base_classes.controllers.sinInverse import ArcSinController
from .base_classes.controllers.tanInverse import ArcTanController
from .base_classes.controllers.exp import ExpController
from .base_classes.controllers.factorial import FactorialController
from .base_classes.controllers.sin import SinController
from .base_classes.controllers.cos import CosController
from .base_classes.controllers.tan import TanController
from .base_classes.controllers.sec import SecController
from .base_classes.controllers.ln import LnController
from .base_classes.controllers.pi import PiController
from .base_classes.controllers.root import RootController
from .base_classes.controllers.plusminus import PlusMinusController
from .base_classes.controllers.mutlipleEquations import MultipleEquationsController
from .base_classes.base import *

# Useful typing saving expressions and constants


def sqrt(expression):
    return Expression(RootController, [expression, Num(2)])


def plusMinus(expression):
    return Expression(PlusMinusController, [expression])


def Sin(expression):
    return Expression(SinController, [expression])


def Cos(expression):
    return Expression(CosController, [expression])


def Tan(expression):
    return Expression(TanController, [expression])


def Sec(expression):
    return Expression(SecController, [expression])


def ArcSin(expression):
    return Expression(ArcSinController, [expression])


def ArcCos(expression):
    return Expression(ArcCosController, [expression])


def ArcTan(expression):
    return Expression(ArcTanController, [expression])


def Exp(expression):
    return expression.exp()


def Factorial(expression):
    return Expression(FactorialController, [expression])

def Ln(expression):
    return Expression(LnController, [expression])


# Constants
pi = Expression(PiController, [])
