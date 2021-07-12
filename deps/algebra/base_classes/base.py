from .controllers.addition import AdditionController
from .controllers.exponentiation import ExponentiationController
from .controllers.multiplication import MultiplicationController
from .controllers.subtraction import SubtractionController
from .controllers.division import DivisionController
from .controllers.number import NumberController
from .controllers.variable import VariableController
from .controllers.ln import LnController
from .controllers.exp import ExpController
from .controllers.sin import SinController
from .controllers.cos import CosController
from .controllers.tan import TanController
from .controllers.sec import SecController
from .unification import Unification
import decimal

# The expression class is used to represent a mathematical expression


class Expression:
    def __init__(self, controller_type, arguments):
        self.arguments = arguments
        self.controller = controller_type(self.arguments)
        self.controller_type = controller_type
        self.castIntegers()

    def substitute(self, variable, value):
        return self.substituteMany(Unification({variable.getName(): value}))

    def getType(self):
        return self.controller.getName()

    def toTex(self, needsBrackets=False, environment=False):
        if self.controller.hasCustomEnvironment() or not environment:
            return self.controller.toTex(needsBrackets, environment)
        else:
            return "\\begin{"+environment+"}"+self.controller.toTex(needsBrackets, environment)+"\\end{"+environment+"}"

    def differentiate(self, target):
        result = self.controller.differentiate(target)
        if(type(result) in [float, int]):
            return Num(result)
        else:
            return result
    # This function exists as a failsafe in case a float/integer is passed in as an argument
    # It converts them into expressions that can be differentiated/rendered to screen

    def castIntegers(self):
        def convert(arg):
            if(type(arg) in [int, float]):
                return Num(arg)
            else:
                return arg
        self.arguments = [convert(arg) for arg in self.arguments]

    # Overiding behaviour for python arithmetic operations

    def __add__(self, other):
        if(type(other) in [int, float]):
            other = Num(other)
        return CommutativeExpression(AdditionController, [self, other])

    def __sub__(self, other):
        if(type(other) in [int, float]):
            other = Num(other)
        return Expression(SubtractionController, [self, other])

    # def __call__(self):
    #     return self.controller.evaluate()

    def __mul__(self, other):
        if(type(other) in [int, float]):
            other = Num(other)
        return CommutativeExpression(MultiplicationController, [self, other])

    # Define x*y=y*x
    __rmul__ = __mul__

    # Define x+y=y+x
    __radd__ = __add__

    def __truediv__(self, other):
        return Expression(DivisionController, [self, other])

    def __rtruediv__(self, other):
        if(type(other) in [float, int]):
            return Expression(DivisionController, [Num(other), self])

    def __pow__(self, other):
        if(type(other) in [float, int]):
            return Expression(ExponentiationController, [self, Num(other)])
        else:
            return Expression(ExponentiationController, [self, other])

    def substituteIntoArguments(self, substitutions):
        newArguments = []
        for argument in self.arguments:
            argWithSub = argument.substituteMany(substitutions)
            if(type(argWithSub) == list):
                newArguments += argWithSub
            else:
                newArguments.append(argWithSub)
        return newArguments

    # Allowing users to substitute into an expression
    def substituteMany(self, substitutions):
        return Expression(self.controller_type, self.substituteIntoArguments(substitutions))

    def getArguments(self):
        return self.arguments

    def getArity(self):
        return len(self.arguments)

    def replaceArguments(self, arguments):
        return Expression(self.controller_type, arguments)

    def ln(self):
        return Expression(LnController, [self])

    def exp(self):
        return Expression(ExpController, [self])

    def sin(self):
        return Expression(SinController, [self])

    def cos(self):
        return Expression(CosController, [self])

    def tan(self):
        return Expression(TanController, [self])

    def sec(self):
        return Expression(SecController, [self])

    def evaluate(self):
        return self.controller.evaluate()

    def unify(self, other):
        selfClone = self
        if self.getType() == other.getType():
            if(self.getArity() == other.getArity()):
                overallUnification = Unification()
                for i in range(len(self.getArguments())):
                    selfArgs = selfClone.getArguments()
                    otherArgs = other.getArguments()
                    unification = selfArgs[i].unify(otherArgs[i])
                    if(not unification):
                        # The two arguments we are trialling are not unifiable
                        # Therefore the two terms as a whole cannot be
                        return False
                    else:
                        # This line is to avoid variables being assigned multiple values
                        # As the variable will be replaced by the new value and not used
                        # In further unification
                        selfClone = selfClone.substituteMany(unification)
                        overallUnification = overallUnification.merge(
                            unification)
                return overallUnification
        return False

    def isSingleTerm(self):
        return len(self.arguments) <= 1

    def canCalculate(self):
        if hasattr(self.controller, 'canCalculate'):
            return self.controller.canCalculate()
        else:
            return all([argument.canCalculate() for argument in self.arguments])

    def functionOf(self, variable):
        return any([argument.functionOf(variable) for argument in self.arguments])

    def getVariables(self):
        variables = []
        for argument in self.arguments:
            argument_variables = argument.getVariables()
            for variable in argument_variables:
                if not variable in variables:
                    variables.append(variable)
        return variables

    def containsController(self, controllerName):
        return self.getType() == controllerName or any([argument.containsController(controllerName) for argument in self.arguments])

    def getControllerType(self):
        return self.controller_type
# The commutative expression class is used to represent a mathematical expression
# In which order doesn't matter


class CommutativeExpression(Expression):
    def unify(self, other, index=0, usedIndices=[], currentUnification=False):
        # Two terms cannot be unified if they are not the same type
        if self.getType() == other.getType():
            if index == other.getArity():
                if len(usedIndices) == len(self.arguments):
                    return Unification()
                else:
                    # If we are at the end of the terms in the other expression
                    # But have not used all of self
                    return False
            currentOtherTerm = other.getArguments()[index]
            for i in range(len(self.arguments)):
                currentSelfTerm = self.arguments[i]
                # Unification aims to return the largest possible (not)function of x if present
                if currentSelfTerm.getType() in ["FunctionOf", "NotFunctionOf"]:
                    if currentUnification and currentUnification.contains(currentSelfTerm):
                        attemptedUnification = currentSelfTerm.unify(
                            currentOtherTerm)
                        if attemptedUnification:
                            existingValue = currentUnification.getVar(
                                currentSelfTerm)
                            # Add the current term to the expression
                            if existingValue.getType() == self.getType():
                                existingArgs = existingValue.getArguments()
                                newValue = CommutativeExpression(
                                    self.controller_type, existingArgs+[currentOtherTerm])
                            else:
                                newValue = CommutativeExpression(
                                    self.controller_type, [existingValue, currentOtherTerm])
                            # Update the unification
                            newUnification = currentUnification.overwrite(
                                currentSelfTerm, newValue)
                            fullUnification = self.unify(
                                other, index+1, usedIndices, newUnification)
                            if fullUnification:
                                return newUnification.merge(fullUnification)
                if not i in usedIndices:
                    termUnification = currentSelfTerm.unify(currentOtherTerm)
                    if(termUnification):
                        if currentSelfTerm.getType() in ["FunctionOf", "NotFunctionOf"]:
                            fullUnification = self.unify(
                                other, index+1, usedIndices+[i], termUnification.merge(currentUnification))
                            if fullUnification:
                                return termUnification.merge(fullUnification)
                        else:
                            selfWithSub = self.substituteMany(termUnification)
                            fullUnification = selfWithSub.unify(
                                other, index+1, usedIndices+[i], termUnification.merge(currentUnification))
                            if fullUnification:
                                return termUnification.merge(fullUnification)

    def substituteMany(self, substitutions):
        return CommutativeExpression(self.controller_type, self.substituteIntoArguments(substitutions))


class Num(Expression):
    def __init__(self, value):
        self.controller_type = NumberController
        self.value = value
        self.arguments = []
        self.controller = self.controller_type(value)

    def __eq__(self, other):
        return type(other) == Num and self.evaluate() == other.evaluate()

    def unify(self, other):
        return Unification() if self == other else False

    def substituteMany(self, unification):
        return self


class Var(Expression):
    def __init__(self, name=False):
        self.controller_type = VariableController
        self.arguments = []
        self.name = name
        self.controller = self.controller_type(name)

    def getName(self):
        if self.name:
            return self.name
        else:
            return 'VAR'+str(id(self))

    def __eq__(self, other):
        return self is other

    def substituteMany(self, substitutions):
        if substitutions.contains(self):
            return substitutions.getVar(self)
        else:
            return self

    def unify(self, other):
        if type(other) == Var:
            if self.getName() == other.getName():
                return Unification()
        return False

    def canCalculate(self):
        return False

    def functionOf(self, var):
        return self.getName() == var.getName()

    def getVariables(self):
        return [self.name]

    def getType(self):
        return "Variable"

    def evaluate(self):
        return self
