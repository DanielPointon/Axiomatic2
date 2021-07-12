import copy

# This is a class to store the substitutions required to make 2 terms logically equivalent
# Objects of this type will come from the unify functions in base.py


class Unification:
    def __init__(self, substitutions={}):
        #copy.deepcopy used to avoid dependence between unifications
        self.substitutions = copy.deepcopy(substitutions)

    def addSubstitutions(self, var, value):
        self.substitutions[var] = value

    def getVar(self, var):
        return self.substitutions[var.getName()]

    def getSubstitutions(self):
        return self.substitutions

    # Combines the unification with another unification
    def merge(self, unification):
        if not unification:
            return self
        substitutions = copy.deepcopy(unification.getSubstitutions())
        new_substitutions = {}
        for key in self.substitutions:
            new_substitutions[key] = self.substitutions[key]
        for key in substitutions:
            new_substitutions[key] = substitutions[key]
        return Unification(new_substitutions)

    def contains(self, var):
        return var.getName() in self.substitutions

    def overwrite(self, var, value):
        substitutions = copy.deepcopy(self.getSubstitutions())
        substitutions[var.getName()] = value
        return Unification(substitutions)
