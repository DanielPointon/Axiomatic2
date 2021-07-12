class AdvancedRule:
    def __init__(self, head, prerequisites, tail, trivial=False):
        self.head = head
        self.tail = tail
        self.trivial = trivial
        self.prerequisites = prerequisites

    def toTex(self):
        return "\\text{Advanced rule}"

    def getHead(self):
        return self.head

    def getTail(self):
        return self.tail

    def isTrivial(self):
        return self.trivial

    def getUnification(self, expression):
        unification = self.getHead().unify(expression)
        if (unification):
            passed_prereqs = (all([prerequisite(unification, expression)
                                   for prerequisite in self.prerequisites]))
            if(passed_prereqs):
                return unification

    def apply(self, expression, targetVariable=False):
        unification = self.getUnification(expression)
        if unification != None:
            return self.tail.substituteMany(unification)
        else:
            return False
