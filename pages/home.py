from model.usersay import UserSay

def Home():
    result = ''
    for msg in ['I love you!', 'S1234', 'test']:
        Bot = UserSay('testUid', msg)
        returnMessages = Bot.dosomething()
        result += '<p>======== ' + Bot.result + ' ===========</p>'
        for item in returnMessages:
            result += str(item) + '<br />'
    
    return result