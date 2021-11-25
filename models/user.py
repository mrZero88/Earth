class User:
    def __init__(self, id, username, first_name, last_name):
        self.id = id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return "[" + self.id + ", " + self.username + ", " + self.first_name + ", " + self.last_name + "]"
