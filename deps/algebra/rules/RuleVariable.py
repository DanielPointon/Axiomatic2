from ..base_classes.base import Var, Num, Expression
from ..base_classes.controllers.variable import VariableController
from ..base_classes.controllers.rulevariable import RuleVarController
from ..base_classes.unification import Unification


class RuleVar(Var):
    def __init__(self, nameTex='p'):
        super()
        self.controller_type = VariableController
        self.arguments = []
        self.controller = self.controller_type(self.arguments)
        self.name = nameTex

    def getName(self):
        return 'RULEVAR'+str(id(self))

    def __eq__(self, other):
        return self is other

    def unify(self, other):
        return Unification({self.getName(): other})

    def getArguments(self):
        return ArgumentsPlaceholder(self)

    def evaluate(self):
        return CalculatePlaceholder(self)

    def getType(self):
        return "RuleVar"

    def toTex(self, needsBrackets=False, environment=False):
        return self.name
    
    def isSingleTerm(self):
        return True


class ArgumentsPlaceholder:
    def __init__(self, var):
        self.var = var

    def substituteMany(self, substitutions):
        if substitutions.contains(self.var):
            return substitutions.getVar(self.var).getArguments()

    def toTex(self, needsBrackets=False):
        return self.var.toTex()+"_{\\text{placeholder}}"

    def getType(self):
        return "ArgumentsPlaceholder"

# Calculate placeholder is used to allow use to evaluate unknown expressions in rules
# Waits until expression is substituted in to evaluate


class CalculatePlaceholder(ArgumentsPlaceholder):
    def substituteMany(self, substitutions):
        if substitutions.contains(self.var):
            # Returns as a Num
            return Num(substitutions.getVar(self.var).evaluate())


class TypedRuleVar(RuleVar):
    def __init__(self, controller_type, name="\\text{Rule Var}"):
        self.controller_type = RuleVarController
        super()
        self.target_type = controller_type
        self.name = name

    def unify(self, other):
        if(other.getType() == self.target_type):
            return super().unify(other)
        else:
            return False

    def toTex(self, needsBrackets=False):
        return self.name


class CalculateableRuleVar(RuleVar):
    def __init__(self):
        self.controller_type = VariableController
        super()

    def unify(self, other):
        # Removed Num
        if(other.canCalculate() and type(other) != Num):
            return super().unify(other)
        else:
            return False

    def toTex(self):
        return "\\text{Calculateable Rule Var}"

# REVIEW THESE VARIABLES RE CONTROLLERS


class FunctionOf(RuleVar):
    def __init__(self, name, var):
        self.var = var
        self.name = name
        super()

    def unify(self, other):
        # Removed Num
        if(other.functionOf(self.var)):
            return super().unify(other)
        else:
            return False

    def toTex(self, needsBrackets=False):
        return " "+self.name+"("+self.var.toTex()+")"

    def getType(self):
        return "FunctionOf"

    def isSingleTerm(self):
        return True


class NotFunctionOf(RuleVar):
    def __init__(self, name, var):
        self.var = var
        self.name = name
        super()

    def unify(self, other):
        # Removed Num
        if(not other.functionOf(self.var)):
            return super().unify(other)
        else:
            return False

    def toTex(self, needsBrackets=False):
        return " "+self.name

    def getType(self):
        return "NotFunctionOf"

    def isSingleTerm(self):
        return True


class Other:
    def __init__(self, name, var):
        def unify(self, other):
            # If the term is being included in a unification call an error has occured, this is just a placeholder
            raise Exception(
                "Other should not be included in a non-commutative expression")

        def toTex(self, needsBrackets=False):
            return "\\text{other}"
