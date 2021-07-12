from ..rules.solvingRules import getSolvingRules
from .simplify import simplify
def solve(equation, variable):
    solvingRules=getSolvingRules(variable)
    return simplify(equation, solvingRules)