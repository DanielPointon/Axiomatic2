from .RuleVariable import RuleVar, TypedRuleVar
from ..base_classes.base import Num
import copy
# Useful functions for collection terms


def insertIntoTable(hash_table, term, count):
    change_made = False
    hash_table = copy.deepcopy(hash_table)
    termTex = term.toTex()
    if termTex in hash_table:
        hash_table[termTex]['count'] += count
        change_made = True
    else:
        hash_table[termTex] = {'expression': term, 'count': count}
    return hash_table, change_made


def convertSingleTerm(expression_data):
    count = expression_data['count']
    expression = expression_data['expression']
    if type(count) == Num and count.evaluate() == 1:
        return expression
    elif type(count) == Num and count.evaluate() == 0:
        return Num(1)
    else:
        return expression_data['expression']**expression_data['count']


def convertHashTableToList(hash_table, function):
    output = []
    for key in hash_table:
        output.append(function(hash_table[key]))
    return output


def genReducedHashTable(terms):
    reduced_hash_table = {}
    change_made = False
    for term in terms:
        base = RuleVar()
        exponent = RuleVar()
        unification = (base**exponent).unify(term)
        if(unification):
            reduced_hash_table, temp_change_made = insertIntoTable(
                reduced_hash_table, unification.getVar(base), unification.getVar(exponent))
        else:
            reduced_hash_table, temp_change_made = insertIntoTable(
                reduced_hash_table, term, Num(1))
        if temp_change_made:
            change_made = True
    return reduced_hash_table, change_made


def splitFraction(fraction):
    numerator = RuleVar()
    denominator = RuleVar()
    unification = (numerator/denominator).unify(fraction)
    if(unification):
        return unification.getVar(numerator), unification.getVar(denominator)
    else:
        return False


def filterRemove(targetList, elemToRemove):
    new_list = []
    for term in targetList:
        if not term == elemToRemove:
            new_list.append(term)
    return new_list
