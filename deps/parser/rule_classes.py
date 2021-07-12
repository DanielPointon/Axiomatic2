from .rule_elements import *
from deps.algebra.base_classes.base import *
from .codeControllers import *
# Experiment in LL(1) Parsing


class ParsingRule:
    count = 0

    def __init__(self, elements, controller, level):
        self.elements = []
        for element in elements:
            if type(element) == str:
                self.elements.append(NonTerminal(element))
            else:
                self.elements.append(element)
        self.elements[0].setFirst(True)
        self.elements[-1].setLast(True)
        self.controller = controller
        self.level = level

    def get_element(self, index):
        if index < len(self.elements):
            return self.elements[index]
        else:
            return False

    def get_controller(self):
        return self.controller

    def getOutput(self, childNodes):
        if not self.get_controller():
            childNodes[0].level = self.level
            return childNodes[0]
        else:
            new_exp = Expression(self.get_controller(), childNodes)
            new_exp.level = self.level
            return new_exp

class LanguageParsingRule:
    count = 0

    def __init__(self, elements, controller):
        self.elements = []
        for element in elements:
            if type(element) == str:
                self.elements.append(NonTerminal(element))
            else:
                self.elements.append(element)
        self.elements[0].setFirst(True)
        self.elements[-1].setLast(True)
        self.controller = controller

    def get_element(self, index):
        if index < len(self.elements):
            return self.elements[index]
        else:
            return False

    def get_controller(self):
        return self.controller

    def getOutput(self, childNodes):
        if not self.get_controller():
            return childNodes[0]
        else:
            new_exp = CodeConstruct(childNodes, self.get_controller())
            return new_exp
