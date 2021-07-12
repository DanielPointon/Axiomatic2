from deps.parser import *
import deps.algebra.functions.solving as solving
from deps.algebra.functions.simplify import simplify
from deps.algebra.base_classes.controllers.derivative import DerivativeController
from deps.algebra.base_classes.controllers.indefiniteIntegral import IndefiniteIntegralController
from deps.media.manim.manimVid import Video, getMovieConfig
import eel
import os
import uuid
from deps.algebra import *
from deps.media.PDF.LaTexFile import Document
from deps.algebra.functions.newtonsMethod import getNewtonsWorkings
from deps.media.manim.trapeziumRule import *

eel.init('deps/gui')

# Interaction Flow: class for controlling the frontend, allowing for asynchronous input


class InteractionFlow:
    sessionType = "interactionFlow"
    phase = "firstUpdate"
    sendResult = True

    def __init__(self, sessionID):
        self.sessionID = sessionID
        self.outgoingInputs = []
        self.outgoingAction = {}
        self.outgoingActionName = ""
    # Function to check for missing inputs

    def checkInputs(self, inputs, required_keys):
        if(all([(key in inputs) and bool(inputs[key]) for key in required_keys])):
            return True
        else:
            self.addAction("Error", {"description": "Missing input"})

        # This takes data to be sent to a user and converts into a single packet that can be sent to the frontend
    def getPacket(self, payload):
        packet = {'sessionID': self.sessionID,
                  'phase': self.phase, 'type': self.sessionType}
        for key in payload:
            packet[key] = payload[key]
        return packet

    # When input is received from a user, this function is called
    def packetHandler(self, packet):
        # try:
        if packet['updateType'] == 'inputs':
            phase = packet['phase']
            phaseHandler = getattr(self, 'on'+phase)
            phaseHandler(packet)
        if packet['updateType'] == 'firstUpdate':
            self.onFirstUpdate(packet)
        # except Exception as e:
        #     self.addAction("Error", {'description': str(e)})
        return self.getResponse()

    def addTextInput(self, input_name, label):
        self.outgoingInputs.append(
            {'type': 'text', 'id': input_name, 'label': label, 'needsFormControl': True})

    def addSelectInput(self, label, input_name, options):
        self.outgoingInputs.append(
            {'type': 'select', 'id': input_name, 'label': label, 'options': options, 'needsFormControl': True})

    def addLatexInput(self, input_name, options):
        self.outgoingInputs.append(
            {'type': 'selectcorrectlatex', 'id': input_name, 'label': "Ambiguous input, please select the correct latex", 'options': options, 'needsFormControl': False})

    def addAction(self, actionName, payload):
        self.outgoingAction = payload
        self.outgoingActionName = actionName

    def addTextareaInput(self, input_name, label):
        self.outgoingInputs.append(
            {'type': 'textarea', 'id': input_name, 'label': label, 'needsFormControl': True})
    # The phase attribute is used in order to keep the client and server in sync
    # The client sends which phase in the interaction flow they are at when sending inputs
    # And the server uses phase to determine which code to run(on{Phase} functions)

    def setNextPhase(self, phase):
        self.phase = phase

    def getResponse(self, reparsedLatex=False):
        if len(self.outgoingInputs) > 0:
            payload = self.getPacket(
                {'action': 'inputNeeded', 'inputs': self.outgoingInputs})
            self.outgoingInputs = []
            return payload
        elif self.outgoingActionName:
            payload = self.getPacket(
                {'action': self.outgoingActionName, 'payload': self.outgoingAction})
            self.outgoingAction = {}
            self.outgoingActionName = ""
            return payload
        else:
            if self.sendResult:
                if reparsedLatex:
                    return self.getPacket({'action': 'resultReady', 'resultTex': self.workings.getResult().toTex(), 'reparsed_input': reparsedLatex})
                else:
                    return self.getPacket({'action': 'resultReady', 'resultTex': self.workings.getResult().toTex()})

    def requestVariableSelection(self):
        variables = self.parsedExpression.getVariables()
        self.addSelectInput('Please select a variable',
                            'variableselect', variables)
        self.setNextPhase("Variableselect")
    def getWorkings(self):
        return self.workings

# This is an interaction flow that takes latex inputs, allows us not to duplicate syntax checking across interactions


class TakesLatex(InteractionFlow):

    def getNewLatex(self):
        return self.newLatex

    # Removes expression with identical latex, parsing can return mutiple expressions that
    # mean the same thing due to associativity of multiplication and addition
    def removeDuplicates(self, options):
        usedTex = {}
        filteredOptions = []
        for option in options:
            optionTex = option.toTex()
            if not (optionTex in usedTex):
                usedTex[optionTex] = True
                filteredOptions.append(option)
        return filteredOptions

    def getResponse(self):
        if len(self.outgoingInputs) > 0:
            payload = self.getPacket(
                {'action': 'inputNeeded', 'inputs': self.outgoingInputs, 'reparsed_input': self.getNewLatex()})
            self.outgoingInputs = []
            return payload
        else:
            return super().getResponse(reparsedLatex=self.getNewLatex())

    def requestLatexSelection(self, latex):
        self.newLatex = latex
        backups = []
        for i in range(len(self.possibleParsings)):
            backups.append([i, self.possibleParsings[i].toTex()])
            self.setNextPhase("LatexSelected")
        self.addLatexInput("latexindex", backups)

    def packetHandler(self, packet):
        if packet['updateType'] == 'firstUpdate':
            if (not packet['latex']):
                self.addAction("Error", {"description": "Empty input"})
            else:
                self.possibleParsings = self.removeDuplicates(ParseObject(
                    standardGrammar).parse(packet['latex'], return_all=True))
                if len(self.possibleParsings) == 1:
                    self.parsedExpression = self.possibleParsings[0]
                    self.newLatex = self.parsedExpression.toTex()
                    self.onFirstUpdate(packet)
                # Multiple options available, ask user which one to use
                elif self.possibleParsings:
                    self.requestLatexSelection(packet['latex'])
                else:
                    # No options available using standard rules, parse less rigorously
                    self.possibleParsings = self.removeDuplicates(ParseObject(moreExpansiveRules).parse(
                        packet['latex'], return_all=True))
                    if self.possibleParsings:
                        self.requestLatexSelection(packet['latex'])
                    else:
                        self.newLatex = packet['latex']
                        self.addAction(
                            "Error", {"description": "Invalid latex"})
            return self.getResponse()
        else:
            # Continue as normal with other phases
            return super().packetHandler(packet)

    def onLatexSelected(self, packet):
        index = int(packet['inputs']['latexindex'])
        self.parsedExpression = self.possibleParsings[index]
        self.newLatex = self.possibleParsings[index].toTex()
        self.onFirstUpdate(packet)


class Solve(TakesLatex):
    sessionType = "solve"

    def onFirstUpdate(self, packet):
        self.requestVariableSelection()

    def onVariableselect(self, packet):
        self.variable = packet['inputs']['variableselect']
        tempResult = solving.solve(self.parsedExpression, Var(self.variable))
        # Function to check if a simplification result contains a valid solution to the problem

        def isSolved(equation, targetVariable):
            if equation.getType() == "MultipleEquations":
                equations = equation.getArguments()
                return any([isSolved(equation, self.variable) for equation in equations])
            else:
                resultLeftHandSide = equation.getArguments()[0]
                return resultLeftHandSide.getType() == "Variable" and resultLeftHandSide.getName() == targetVariable
        if(tempResult.getResult().getType() == "MultipleEquations"):
            equations = tempResult.getResult().getArguments()
            if(any([isSolved(equation, self.variable) for equation in equations])):
                self.workings = tempResult
        else:
            if(tempResult.getResult().getType() == "Equation"):
                resultLeftHandSide = tempResult.getResult().getArguments()[0]
                # If equation is now of the form x=answer
                if resultLeftHandSide.getType() == "Variable" and resultLeftHandSide.getName() == self.variable:
                    self.workings = tempResult
        if not hasattr(self, 'workings'):
            self.addSelectInput(
                "Cannot solve analytically, would you like to use newton's method instead?", "usenewtons", ["Yes", "No"])
            self.setNextPhase("NewtonsMethod")

    def onNewtonsMethod(self, packet):
        newtons = packet['inputs']['usenewtons']
        if newtons == "Yes":
            self.workings = getNewtonsWorkings(
                self.parsedExpression, Var(self.variable))


class Differentiate(TakesLatex):
    sessionType = "differentiate"

    def getNewLatex(self):
        if hasattr(self, 'variable'):
            # Show the expression they're differentiating with the derivative notation
            return "\\frac{d}{d"+self.variable+"}("+self.newLatex+")"
        else:
            return self.newLatex

    def onFirstUpdate(self, packet):
        self.requestVariableSelection()

    def onVariableselect(self, packet):
        self.variable = packet['inputs']['variableselect']
        self.workings = simplify(
            Expression(DerivativeController, [Var(self.variable), self.parsedExpression]), TrivialRules)


class IntegrateFlow(TakesLatex):
    sessionType = "integrate"

    def onFirstUpdate(self, packet):
        self.requestVariableSelection()

    def onVariableselect(self, packet):
        self.variable = packet['inputs']['variableselect']
        integral = Expression(IndefiniteIntegralController, [
                              self.parsedExpression, Var(self.variable)])
        self.workings = simplify(integral, TrivialRules)


class Simplify(TakesLatex):
    sessionType = "simplify"

    def onFirstUpdate(self, packet):
        self.workings = simplify(self.parsedExpression, TrivialRules)


class MiniTerminal(InteractionFlow):
    sessionType = "MiniTerminal"

    def __init__(self, sessionID):
        super().__init__(sessionID)
        self.state = LanguageState()

    def execute(self, parsingResult):
        if(issubclass(type(parsingResult), Expression)):
            return simplify(self.state.evaluateExpression(parsingResult), TrivialRules).getResult().toTex()
        else:
            self.state = parsingResult.execute(self.state)
            return "\\text{Done}"

    def onFirstUpdate(self, packet):
        self.addAction('newCodeSession', {})
        self.setNextPhase("NewUpdate")

    def onNewUpdate(self, packet):
        if(packet['inputs']['code'] == 'done();'):
            self.workings = self.state.output
        else:
            parsingResult = ParseObject(languageRules).parse(
                packet['inputs']['code'])
            if parsingResult:
                output = self.execute(parsingResult)
            else:
                output = "\\text{Cannot parse}"
            self.addAction('newCodeResult', {
                           'input': packet['inputs']['code'], 'output': output})


class VideoFlow(InteractionFlow):
    sessionType = "video"
    sendResult = False

    def __init__(self, sessionID, sessions):
        super().__init__(sessionID)
        self.sessions = sessions

    def onFirstUpdate(self, packet):
        self.addSelectInput(
            "Would you like to save the video?", "savevideo", ["Yes", "No"])
        self.setNextPhase("SaveVideoDecisionMade")
        self.solutionSessionID = packet['solutionSessionID']

    def onSaveVideoDecisionMade(self, packet):
        self.saveVideo = packet['inputs']['savevideo'] == "Yes"
        if(self.saveVideo):
            self.addTextInput("filename", "Choose a filename")
            self.setNextPhase("ReadyToRender")
        else:
            self.onReadyToRender(packet)

    def onReadyToRender(self, packet):
        if 'filename' in packet['inputs']:
            filename = packet['inputs']['filename']
        else:
            filename = False
        solution = self.sessions.getSession(self.solutionSessionID).getWorkings()
        Video(solution, **getMovieConfig(self.saveVideo,
                                         {'filename': filename})).run()


class PDFFlow(InteractionFlow):
    sessionType = "pdf"
    sendResult = False

    def __init__(self, sessionID, sessions):
        super().__init__(sessionID)
        self.sessions = sessions

    def onFirstUpdate(self, packet, usingLegacy=False):
        self.solutionSessionID = packet['solutionSessionID']
        self.addTextInput("filename", "What filename would you like?")
        self.addTextInput("title", "What title would you like?",)
        self.addTextInput("author", "What author name would you like?")
        self.setNextPhase("ReadyToRender")

    def onReadyToRender(self, packet):
        solution = self.sessions.getSession(self.solutionSessionID).workings
        safeToRender = self.checkInputs(
            packet['inputs'], ['filename', 'title', 'author'])
        if safeToRender:

            Paper = Document(packet['inputs']['filename'],
                             packet['inputs']['title'], packet['inputs']['author'])
            Paper.addWorkings(solution)
            Paper.render()


class Sessions:
    sessionTypes = {
        'solve': {'sessionClass': Solve, 'requiresSelf': False},
        'differentiate': {'sessionClass': Differentiate, 'requiresSelf': False},
        'simplify': {'sessionClass': Simplify, 'requiresSelf': False},
        'pdf': {'sessionClass': PDFFlow, 'requiresSelf': True},
        'video': {'sessionClass': VideoFlow, 'requiresSelf': True},
        'integrate': {'sessionClass': IntegrateFlow, 'requiresSelf': False},
        'miniTerminal': {'sessionClass': MiniTerminal, 'requiresSelf': False},
    }

    def __init__(self):
        self.sessions = {}

    def addSession(self, packet):
        sessionID = str(uuid.uuid4())
        if packet['task'] in self.sessionTypes:
            sessionData = self.sessionTypes[packet['task']]
            if sessionData['requiresSelf']:
                self.sessions[sessionID] = sessionData['sessionClass'](
                    sessionID, self)
            else:
                self.sessions[sessionID] = sessionData['sessionClass'](
                    sessionID)
        else:
            raise Exception("Invalid data from frontend-session not found")
        return sessionID

    def handlePacket(self, packet):
        if 'sessionID' in packet:
            return self.sessions[packet['sessionID']].packetHandler(packet)
        else:
            sessionID = self.addSession(packet)
            return self.sessions[sessionID].packetHandler(packet)

    def getSession(self, sessionID):
        return self.sessions[sessionID]


# EXPERIMENTAL

sessions = Sessions()


@eel.expose
def getInputs(packet):
    return sessions.handlePacket(packet)


eel.start('main.html', size=(800, 800))
