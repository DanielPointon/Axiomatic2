from deps.algebra.base_classes.base import *
from .codeControllers import *
import string


class ParsingElement:
    last = False
    first = False

    def setFirst(self, first):
        self.first = first

    def setLast(self, last):
        self.last = last

    def isLast(self):
        return self.last

    def isAtomic(self):
        return False

    def includedInResult(self):
        return True


class Atomic(ParsingElement):
    def isAtomic(self):
        return True


class ParsingNumber(Atomic):
    def isValid(self, string):
        if string[0] in ['+', '.']:
            return False
        try:
            float(string)
        except:
            return False
        return True

    def parse(self, string):
        if self.isValid(string):
            parsing = float(string)
            return Num(parsing), len(string)
        else:
            return False

class ParsingString(Atomic):
    def parse(self, string):
        if string.isalnum():
            return string, len(string)
        else:
            return False

class ParsingStringPlaceholder(ParsingElement):
    def matches(self, element):
        # return True
        return type(element)==str

    def __str__(self):
        return "ParsingString"

class ParsingVariable(Atomic):
    # Certain letters have pre-defined mathematical meanings and so cannot be used as variable names
    legal_variables = [char for char in list(
        string.ascii_lowercase) if char not in ["e", "i"]]+["\\lambda", "\\theta"]

    def __init__(self):
        self.type = "Exp"
        self.terminal_status = False
        self.last = False

    def parse(self, string):
        if(string in self.legal_variables):
            return Var(string), len(string)
        else:
            return False


class NonTerminal(Atomic):
    def __init__(self, string):
        self.string = string

    def parse(self, string):
        if string[:len(self.string)] == self.string:
            return self.string, len(self.string)
        else:
            return False

    def includedInResult(self):
        return False


class TermOfLevel(ParsingElement):
    def __init__(self, level):
        self.level = level

    def isAtomic(self):
        return False

    def matches(self, element):
        # return True
        if not hasattr(element, 'level'):
            return self.level <= 100

        if self.level <= element.level:
            return True

    def __str__(self):
        return "TermOfLevel"+str(self.level)

class ExpressionOfLevel(ParsingElement):
    def __init__(self, level):
        self.level = level

    def isAtomic(self):
        return False

    def matches(self, element):
        # return True
        if not hasattr(element, 'level'):
            return self.level <= 100

        if self.level <= element.level:
            return True

    def __str__(self):
        return "ExpressionOfLevel"+str(self.level)

class TermWithController(ParsingElement):
    def __init__(self, controller_type):
        self.controller_type = controller_type

    def matches(self, expression):
        if hasattr(expression, 'getType'):
            return expression.getType() == self.controller_type.name
        else:
            return False
    
    def __str__(self):
        return "TermWithController"+self.controller_type.name



class CodeExpression(Expression, ParsingElement):
    def __init__(self):
        pass

    def matches(self, expression):
        return issubclass(type(expression), Expression) or issubclass(type(expression), CodeExpression)

    def __str__(self):
        return "CodeExp"

class CodeConstructPlaceholder(ParsingElement):
    def matches(self, expression):
        return type(expression) == CodeConstruct
    
    def __str__(self):
        return "CodeConstruct"
