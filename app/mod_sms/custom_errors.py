class DuplicateUserGroupException(Exception):
    def __init___(self):
        Exception.__init__(self,"Duplicate User group already active")
