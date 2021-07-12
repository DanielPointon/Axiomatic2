from ..base_classes.base import Var
from ..rules.RuleVariable import FunctionOf, NotFunctionOf
from ..equation import Equation
from ..base_classes.simplification import Workings, Step, EmptyStep
#THE ALGORITHM THAT MAKES THE CODE COOL
def simplifyOnce(term, rules, targetVariable=False):
    arguments = term.getArguments()
    for i in range(len(arguments)):
        simplification_result = simplifyOnce(arguments[i], rules, targetVariable)
        if simplification_result.ruleApplied():
            return Step(term, term.replaceArguments(list(map(
                lambda arg: simplification_result.expressionAfter if arg[0] == i else arg[1]
            , enumerate(term.getArguments())))), simplification_result.rule)
    for rule in rules:
        application = rule.apply(term, targetVariable)
        if application:
            return Step(term, application, rule)
    return EmptyStep(term)

def simplify(term,rules, targetVariable=False):
    workings=Workings()
    workings=workings.withStep(EmptyStep(term))
    ruleApplied=True
    while ruleApplied:
        tempRuleApplied=False
        simplificationStep=simplifyOnce(term,rules,targetVariable)
        if simplificationStep.ruleApplied():
            tempRuleApplied=True
            workings=workings.withStep(simplificationStep)
            term=simplificationStep.expressionAfter
        ruleApplied=tempRuleApplied
    return workings

