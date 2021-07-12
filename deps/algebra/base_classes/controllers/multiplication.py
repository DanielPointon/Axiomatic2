from .controller import Controller
from functools import reduce


class MultiplicationController(Controller):
    name = 'Multiplication'

    def evaluate(self):
        return reduce(lambda a, b: a*b.evaluate(), self.arguments, 1)

    def differentiate(self, VarName):
        if(len(self.arguments) == 0):
            return Num(0)
        if(len(self.arguments) == 1):
            return self.arguments[0].differentiate(VarName)
        else:
            currentDerivative = self.arguments[0]*self.arguments[1].differentiate(
                VarName)+self.arguments[1]*self.arguments[0].differentiate(VarName)
            for i in range(2, len(self.arguments)):
                currentDerivative = currentDerivative * \
                    self.arguments[i].differentiate(
                        VarName)+self.arguments[i]*currentDerivative.differentiate(VarName)
            return currentDerivative

    def toTex(self, needsBrackets=False, environment=False):
        digits = [str(i) for i in range(0, 9)]
        numbers = list(filter(lambda argument: argument.getType()== "Number", self.arguments))
        numbersString = '\\times '.join([argument.toTex(True) for argument in numbers])
        nonNumbers = list(filter(lambda argument: not argument.getType() == "Number", self.arguments))
        nonNumbersString = ''.join([argument.toTex(True) for argument in nonNumbers])
        if(numbersString == "-1"):
            numbersString = "-"
        if nonNumbersString and ((nonNumbersString[0] in digits) or (nonNumbersString[0] == "{" and (nonNumbersString[1] in digits))):
            if numbersString:
                return numbersString+"\\times"+nonNumbersString
            else:
                return nonNumbersString
        else:
            return numbersString+nonNumbersString
