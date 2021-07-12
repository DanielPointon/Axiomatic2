class DummyExpression:
    def __init__(self, controller_type):
        self.controller_type=controller_type
    def getType(self):
        return self.controller_type.name

class DummyCodeExpression:
    def __init__(self, controller_type):
        self.controller_type=controller_type
    def getType(self):
        return self.controller_type.name