

class User:
    def __init__(self, login, password, name, access='1', email=None, ws=None):
        self.login = login
        self.name = name
        self.password = password
        self.access = access
        self.email = email
        self.ws = ws