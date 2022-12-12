class BotBrain:

    def __init__(self, uid, msg):
        self.uid = uid
        self.msg = msg
        self.result = ''

    def thinking(self):
        self.result = self.uid + 'say:' + self.msg
        return self.result



