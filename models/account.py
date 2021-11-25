import datetime

from datetime import datetime


class Account:
    def __init__(self,
                 id=None,
                 name="",
                 email="",
                 user_name="",
                 password="",
                 provider="",
                 imap="",
                 created_at=None,
                 is_default=False
                 ):
        self.id = id
        self.name = name
        self.email = email
        self.user_name = user_name
        self.password = password
        self.provider = provider
        self.imap = imap
        self.created_at = created_at
        self.is_default = is_default

    def get_formated_created_date_time(self):
        dt = datetime.utcfromtimestamp(self.created_at)
        return dt.strftime("%d %b %y %H:%M:%S")
