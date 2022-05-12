class mockModel():
    files={"model.flite":None}
    def __init__(self):
        pass

class mock_serviceCommands():
    def __init__(self):
        pass
    def getModel(self, modelName):
        return mockModel()
