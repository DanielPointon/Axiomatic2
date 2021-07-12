from deps.algebra.base_classes.base import *
from deps.algebra.base_classes.controllers.equation import EquationController
from deps.algebra.base_classes.controllers.definiteIntegral import DefiniteIntegralController
from deps.algebra.base_classes.controllers.derivative import DerivativeController

from deps.algebra.functions.solving import solve
from deps.algebra.functions.simplify import simplify
from deps.algebra.equation import Equation
from deps.algebra.rules.trivialRules import TrivialRules
from deps.algebra.base_classes.controllers.pi import PiController
from deps.algebra.base_classes.controllers.e import EController
from .rule_classes import *
from .codeControllers import *
from .languageState import LanguageState
from deps.algebra.base_classes.controllers.absolute import AbsController
from deps.algebra.utils import *
# These are the standard rules used to parse mathematical expressions
standardGrammar = [
    ParsingRule([ParsingNumber()], False, 100),
    ParsingRule([ParsingVariable()], False, 100),
    ParsingRule(['(', ExpressionOfLevel(0), ')'], False, 100),
    ParsingRule([ExpressionOfLevel(1.5), '+', ExpressionOfLevel(1.5)],
                controller=AdditionController, level=1.5),
    ParsingRule([ExpressionOfLevel(1), '-', ExpressionOfLevel(1)],
                controller=SubtractionController, level=1),
    ParsingRule([ExpressionOfLevel(2), ExpressionOfLevel(2)],
                controller=MultiplicationController, level=2),
    ParsingRule([ExpressionOfLevel(0), "=", ExpressionOfLevel(0)],
                controller=EquationController, level=-1),
    ParsingRule([ExpressionOfLevel(3), '\\times', ExpressionOfLevel(3)],
                controller=MultiplicationController, level=3),
    ParsingRule([ExpressionOfLevel(3), '/', ExpressionOfLevel(3)],
                controller=DivisionController, level=3),
    ParsingRule([ExpressionOfLevel(0), '^{', ExpressionOfLevel(
        0), "}"], controller=ExponentiationController, level=100),
    ParsingRule(['{', ExpressionOfLevel(0), '}^{', ExpressionOfLevel(
        0), "}"], controller=ExponentiationController, level=100),
    ParsingRule(['e^{', ExpressionOfLevel(0), '}'],
                controller=ExpController, level=100),
    #Trig function syntax definition
    ParsingRule(['\sin(', ExpressionOfLevel(0), ')'],
                controller=SinController, level=100),
    ParsingRule(['\sin^{-1}(', ExpressionOfLevel(0), ')'],
                controller=ArcSinController, level=100),
    ParsingRule(['\cos(', ExpressionOfLevel(0), ')'],
                controller=CosController, level=100),
    ParsingRule(['\cos^{-1}(', ExpressionOfLevel(0), ')'],
                controller=ArcCosController, level=100),
    ParsingRule(['\ln(', ExpressionOfLevel(0), ')'],
                controller=LnController, level=100),
    ParsingRule(['\\tan(', ExpressionOfLevel(0), ')'],
                controller=TanController, level=100),
    ParsingRule(['\\tan^{-1}(', ExpressionOfLevel(0), ')'],
                controller=ArcTanController, level=100),           
    ParsingRule(['\int_{', ExpressionOfLevel(0), '}^{', ExpressionOfLevel(0), '}', ExpressionOfLevel(0), 'd', ParsingVariable()],
                controller=DefiniteIntegralController, level=100),
    ParsingRule(['d/d', TermWithController(VariableController), '(', ExpressionOfLevel(0), ')'],
                controller=DerivativeController, level=100),
    ParsingRule(['d/d', TermWithController(VariableController), '[', ExpressionOfLevel(0), ']'],
                controller=DerivativeController, level=100),

    ParsingRule(['\\pi'], controller=PiController, level=100),

    # ParsingRule(['e'], controller=EController, level=100),
    ParsingRule(['|',ExpressionOfLevel(0), '|' ], controller=AbsController, level=100),

]


# These are rules for parsing expressions with ambiguous exponentiation
moreExpansiveRules = standardGrammar+[ParsingRule([ExpressionOfLevel(
    0), '^', ExpressionOfLevel(0)], controller=ExponentiationController, level=100)]

# These are the rules for parsing expressions enterred into the terminal
languageRules = [
    LanguageParsingRule(['for(', TermWithController(LineOfCodeController), CodeExpression(), ';', TermWithController(
        LineOfCodeController), ')', '{', CodeConstructPlaceholder(), '}'], ForLoopController),
    LanguageParsingRule([CodeConstructPlaceholder(),
                         CodeConstructPlaceholder()], CodeBlockController),
    LanguageParsingRule([TermWithController(
        CodeBlockController), CodeConstructPlaceholder()], CodeBlockController),
    LanguageParsingRule(['if(', CodeExpression(
    ), '){', CodeConstructPlaceholder(), '}'], IfStatementController),
    LanguageParsingRule(
        [TermWithController(EquationController), ';'], LineOfCodeController),
    LanguageParsingRule(['\\', TermWithController(VariableController), '(', TermWithController(
        VariableController), '){', CodeConstructPlaceholder(), '}'], MethodDefinitionController),
    LanguageParsingRule(
        ['\\output(', CodeExpression(), ');'], OutputController),
    LanguageParsingRule(['\\', TermWithController(
        VariableController), '(', ExpressionOfLevel(0), ');'], CallMethodController),

    LanguageParsingRule(
        ['\\output_raw(', CodeExpression(), ');'], OutputRawController),
    ParsingRule([ExpressionOfLevel(0), '<', ExpressionOfLevel(0)],
                LessThanController, level=-1),
    ParsingRule([ExpressionOfLevel(0), '>', ExpressionOfLevel(0)],
                GreaterThanController, level=-1),
]+standardGrammar