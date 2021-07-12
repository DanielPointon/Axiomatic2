from .FunctionalRule import *
from ..base_classes.base import *
from .RuleVariable import RuleVar
from .RuleVariable import TypedRuleVar
from ..base_classes.base import NumberController
from ..base_classes.controllers.addition import AdditionController
from ..base_classes.controllers.division import DivisionController
from .collectionUtils import *
import copy


def decompose(term):
    base = RuleVar()
    exponent = RuleVar()
    unification = (base**exponent).unify(term)
    if(unification):
        return {'expression': unification.getVar(base), 'count': unification.getVar(exponent)}
    else:
        return {'expression': term, 'count': Num(1)}


def getFactors(term):
    if(term.getType() == "Multiplication"):
        return term.getArguments()
    else:
        return [term]


def simplifyExpression(expression, substitution):
    numerator_terms = {}
    denominator_terms = {}
    change_made = False
    for argument in getFactors(substitution.getVar(numerator)):
        decomposed_term = decompose(argument)
        numerator_terms, change_made = insertIntoTable(
            numerator_terms, decomposed_term['expression'], decomposed_term['count'])
    for argument in getFactors((substitution.getVar(denominator))):
        decomposed_term = decompose(argument)
        denominator_terms, change_made = insertIntoTable(
            denominator_terms, decomposed_term['expression'], decomposed_term['count'])
    rule_applied = False
    for term in numerator_terms:
        if term in denominator_terms:
            term_in_numerator = numerator_terms[term]
            term_in_denominator = denominator_terms[term]
            cantCalculateCounts = not(term_in_numerator['count'].canCalculate(
            ) and term_in_denominator['count'].canCalculate())
            rule_applied = True
            if cantCalculateCounts or term_in_numerator['count'].evaluate() > term_in_denominator['count'].evaluate():
                numerator_terms[term]['count'] -= term_in_denominator['count']
                denominator_terms[term]['count'] = Num(0)
            elif term_in_numerator['count'].evaluate() < term_in_denominator['count'].evaluate():
                denominator_terms[term]['count'] -= term_in_numerator['count']
                numerator_terms[term]['count'] = Num(0)
            else:
                numerator_terms[term]['count'] = Num(0)
                denominator_terms[term]['count'] = Num(0)
    numerator_terms_list = filterRemove(convertHashTableToList(
        numerator_terms, convertSingleTerm), Num(1))
    denominator_terms_list = filterRemove(convertHashTableToList(
        denominator_terms, convertSingleTerm), Num(1))
    if rule_applied or change_made:
        # Taking shortcuts when cancelling
        if(len(numerator_terms_list) == 0 and len(denominator_terms_list) == 0):
            return Num(1)
        if(len(numerator_terms_list) == 0):
            return Num(1)/CommutativeExpression(MultiplicationController, denominator_terms_list)
        if(len(denominator_terms_list) == 0):
            return CommutativeExpression(MultiplicationController, numerator_terms_list)
        return CommutativeExpression(MultiplicationController, numerator_terms_list)/CommutativeExpression(MultiplicationController, denominator_terms_list)
    else:
        return False

#Rule applies to fractions with a product as their numerator
numerator = TypedRuleVar("Multiplication")
denominator = RuleVar()

fractionCancellationRule = FunctionalRule(
    numerator/denominator, [], simplifyExpression, "fraction cancellation")
