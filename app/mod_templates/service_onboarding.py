def welcome_1():
    """
    Onboarding step 1:
        Welcome the user to the service, get consent
        from the user to start using the service and
        approval to open an account in their phone
        number.
    """
    resp = '''Welcome to Broadcast! Broadcast is a messaging service
    to keep you in touch with the groups and people that matter
    to you! Broadcast is a free service with premium options; it is
    free to start, free to use, free to join as many groups as you
    choose, and free to create up to 2 groups.

    If you would like to join, please respond "JOIN" for more
    information, respond "OUT" to opt out of all future invitations,
    or simply ignore this message.
    '''
    return resp


def welcome_2():
    """
    Onboarding step 2:
        Explain the service to the user, outline
        'Help' as well as other common keywords.
        Give link to the website
    """
    resp = '''
    Thanks for joining Broadcast! Broadcast works by creating a
    phone number for each group that you or your friends create.
    You will receive messages from those groups that you are
    active in, and can invite friends to the current group with
    the command "BC add [phone number]". For everything else you
    can text "BC Help" and Broadcast will help you out! Please
    respond with your First Name and Last Initial to complete
    your account creation!
    '''
    return resp


def confirm_welcome_2():
    """
    Confrim the user's first and last name
    """
    resp = '''

    '''
    return resp
