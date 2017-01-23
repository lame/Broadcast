class DuplicateUserGroupException(Exception):
    def __init___(self):
        Exception.__init__(self,"Duplicate User group already created and active")

class DuplicateUserException(Exception):
    def __init___(self):
        Exception.__init__(self,"Duplicate User already created and active")

class DuplicateMessageException(Exception):
    def __init___(self):
        Exception.__init__(self,"Duplicate Message already created")
