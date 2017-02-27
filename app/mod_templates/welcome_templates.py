def welcome_to_service():
    resp = '''
    Welcome to Broadcast! We make group messaging
    easier. Text "YES" to join the conversation and
    receive more info!

    Standard carrier text messaging rates apply
    '''
    return resp


def invited_welcome_to_service(user, user_group):
    if user.lname:
        if user.fname:
            name = '{fname} {lname}'.format(fname=user.fname, lname=user.lname)
        name = '{fname}'.format(fname=user.fname)

    resp = '''
    Welcome to Broadcast! We make group messaging
    easier. Your friend {name} invited you to the
    {group_name} group. Text "YES" to join the
    conversation and receive more info!

    Standard carrier text messaging rates apply
    '''.format(name=name, group_name=user_group.name)
    return resp


def get_name():
    resp = '''
    Almost there! What should we call you? Text us your
    name as "Last, First"
    '''
    return resp


def get_email(fname):
    resp = '''
    You're in {fname}! We need your email address just in
    case we need to verify who you are.
    Please text back with your email address.
    '''.format(fname=fname)
    return resp


def invited_user_explain_service():
    resp = '''
    Each Group uses a unique phone number, best to
    label this one now. Text "broadcast help"
    for Text Commands. Enough reading, say
    Wazzup to the group and get going!
    '''
    return resp
