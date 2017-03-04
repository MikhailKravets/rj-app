

class User:
    def __init__(self, name, password, access='1', ws=None):
        self.name = name
        self.password = password
        self.access = access
        self.ws = ws