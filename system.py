

class User:
    def __init__(self, id_user, login, password, name, access='1', email=None, ws=None):
        self.id_user = id_user
        self.login = login
        self.name = name
        self.password = password
        self.access = access
        self.email = email
        self.ws = ws