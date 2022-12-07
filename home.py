from module import *

def processIndex():
    result = ''
    for msg in ['I love you!', 'S1234', 'test', 'test3', 'test4', 'test5', 'test6']:
        Bot = UserSay(msg)
        message = Bot.process()
        result += '<p>' + Bot.result + '</p>'
    
    return result