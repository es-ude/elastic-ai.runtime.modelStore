class MockMessage:
    def __init__(self, msg_str: str):
        self.payload = bytes(msg_str, "utf-8")
