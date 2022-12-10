class UserSpeak:
    uid = ''
    msg = ''
    result = ''

    def __init__(self, uid, msg):
        self.uid = uid
        self.msg = msg

    def process(self):
        self.result = self.uid + 'say:' + self.msg
        return self.result



