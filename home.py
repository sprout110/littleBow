from module import *

def processIndex():
    result = ''
    for msg in ['I love you!', 'S1234', 'test', 'test3', 'test4', 'test5', 'test6', 'test7']:
        Bot = UserSay(msg)
        returnMessage = Bot.process()
        result += '<p>======== ' + Bot.result + ' ===========</p>'
        for item in returnMessage:
            result += str(item) + '<br />'
    
    return result