class mockMessage():
    def __init__(self, msgStr:str):     
        self.payload = bytes(msgStr, 'utf-8')