from model.usersay import UserSay
from matplotlib import font_manager

def Home():
    result = ''
    for msg in ['I love you!', 'S1234', 'test']:
        Bot = UserSay('testUid', msg)
        returnMessages = Bot.dosomething()
        result += '<p>======== ' + Bot.result + ' ===========</p>'
        for item in returnMessages:
            result += str(item) + '<br />'
    
    font_set = {f.name for f in font_manager.fontManager.ttflist}
    for f in font_set:
        result += str(f) + '<br />'
        
    return result