import model.user as user

def home():
    result = ''
    for msg in ['I love you!', 'S1234', 'test', 'test3', 'test4', 'test5', 'test6', 'test7']:
        Brain = user.UserSay('testUid', msg)
        returnMessages = Brain.thinking()
        result += '<p>======== ' + Brain.result + ' ===========</p>'
        for item in returnMessages:
            result += str(item) + '<br />'
    
    return result