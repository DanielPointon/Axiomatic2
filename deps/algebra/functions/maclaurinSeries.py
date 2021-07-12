from ..base_classes import *

def zeroValue(func, target_var):
    return func.substitute(target_var, Num(0))
def TaylorSeries(func, target_var, depth):
    sum = Num(0)
    currentDerivative = simplify(func,TrivialRules).getResult()
    for i in range(depth):
        scalarMultiplier = Num(1)/Factorial(Num(i))
        sum += zeroValue(func, target_var) * (scalarMultiplier) * (Var('x')**Num(i))
        currentDerivative = simplify(currentDerivative.differentiate('x'),TrivialRules).getResult()
    return sum

