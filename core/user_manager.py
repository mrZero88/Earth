from models.user import User
from utils.command import Command


class UserManager:
    def __init__(self, conn):
        self.conn = conn
        self.user = None

    def load_user(self):
        if self.exists_users():
            self.load_user_from_database()
        else:
            self.load_user_from_computer()
            self.insert_user_in_database()

    def exists_users(self):
        cur = self.conn.cursor()
        row = cur.execute("select * from users").fetchone()
        return True if row else False

    def insert_user_in_database(self):
        if self.user is not None:
            cur = self.conn.cursor()
            cur.execute(
                "insert into users values ('" +
                self.user.id + "', '" +
                self.user.username + "', '" +
                self.user.first_name + "', '" +
                self.user.last_name + "')")
            self.conn.commit()

    def load_user_from_database(self):
        cur = self.conn.cursor()
        row = cur.execute("select * from users").fetchone()
        self.user = User(row[0], row[1], row[2], row[3])

    def load_user_from_computer(self):
        user_id, username, user_names = self.get_user_data()
        first_name, last_name = user_names.split()
        self.user = User(user_id, username, first_name, last_name)

    def get_user_data(self):
        command = "grep $(whoami) /etc/passwd | tr -s \":\" | awk -F '[:,]' '{print $3\",\"$1\",\"$5}'"
        output = Command.run_command_with_output_nosplit(command)
        return output.split(",")

    def get_user(self):
        return self.user
