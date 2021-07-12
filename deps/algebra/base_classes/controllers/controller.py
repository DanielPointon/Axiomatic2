class Controller:
    customEnvironmentStatus = False

    def __init__(self, arguments):
        self.arguments = arguments

    def __eq__(self, other):
        return self.name == other.name

    def getName(self):
        return self.name

    def hasCustomEnvironment(self):
        return self.customEnvironmentStatus

    
class ControllerWithInner(Controller):
    def __init__(self, arguments):
        super().__init__(arguments)
        self.inner, = arguments
