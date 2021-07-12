import copy
from .FunctionalRule import *
from ..base_classes.base import *
from .RuleVariable import RuleVar
from .RuleVariable import TypedRuleVar
from ..base_classes.base import NumberController
from ..base_classes.controllers.addition import AdditionController
from ..base_classes.controllers.multiplication import MultiplicationController
from .collectionUtils import *

def simplifyExpression(expression, substitution):
    fraction_broke = False
    numeratorTerms = []
    denominatorTerms = []
    for argument in expression.getArguments():
        splitFractionAttempt = splitFraction(argument)
        if(splitFractionAttempt):
            # Flag a change being made
            fraction_broke = True
            numerator, denominator = splitFractionAttempt
            numeratorTerms.append(numerator)
            denominatorTerms.append(denominator)
        else:
            numeratorTerms.append(argument)
    num_reduced_hash_table, num_change_made = genReducedHashTable(
        numeratorTerms)
    denom_reduced_hash_table, denom_change_made = genReducedHashTable(
        denominatorTerms)
    converted_numerator_terms = convertHashTableToList(
        num_reduced_hash_table, convertSingleTerm)
    converted_denominator_terms = convertHashTableToList(
        denom_reduced_hash_table, convertSingleTerm)
    # If a change has been made to numerator or denominator or a fraction has been broken
    if num_change_made or denom_change_made or fraction_broke:
        # If there are no denominator terms
        if(not converted_denominator_terms):
            return CommutativeExpression(MultiplicationController, converted_numerator_terms)
        else:
            return CommutativeExpression(MultiplicationController, converted_numerator_terms)/CommutativeExpression(MultiplicationController, converted_denominator_terms)
    else:
        return False


productCollectionRule = FunctionalRule(
    TypedRuleVar("Multiplication"), [], simplifyExpression, "commutivity of multiplication")
