#User class

class User:
    def __init__(self):
        self.username = ''

    def input_username(self, username):
        self.username = username
    
    def get_username(self):
        return self.username