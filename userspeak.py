class UserSpeak:
    msg = ''
    result = ''
    def __init__(self, msg):
        self.msg = msg
    def process(self):
        self.result = self.msg
        return [self.msg]



