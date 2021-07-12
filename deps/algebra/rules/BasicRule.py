from ..base_classes.base import *
from .RuleVariable import RuleVar


class BasicRule:
    def __init__(self, head, tail, trivial=False):
        self.head = head
        self.tail = tail
        self.trivial = trivial

    def toTex(self):
        return "\\text{the formula }"+self.head.toTex()+"\space \implies \space "+self.tail.toTex()

    def getHead(self):
        return self.head

    def getTail(self):
        return self.tail

    def isTrivial(self):
        return self.trivial

    def getUnification(self, expression):
        return self.getHead().unify(expression)

    def apply(self, expression, targetVariable=False):
        unification = self.getUnification(expression)
        if unification:
            return self.tail.substituteMany(unification)
        else:
            return False
