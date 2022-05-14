class mockModel():
    #files={"model.flite":None}
    files={"model.flite":0}
    def __init__(self):
        pass

class mock_serviceCommands():
    def __init__(self):
        pass
    def getModel(self, modelName):
        return mockModel()
