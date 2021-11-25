import datetime

from datetime import datetime


class Email:
    def __init__(self,
                 id=None,
                 from_name="",
                 email_from="",
                 to="",
                 subject="",
                 text="",
                 file_path="",
                 cc=None,
                 date=None,
                 account_id=""):
        self.id = id
        self.from_name = from_name
        self.email_from = email_from
        self.to = to
        self.subject = subject
        self.text = text
        self.file_path = file_path
        self.cc = cc
        self.date = date
        self.account_id = account_id

    def get_formated_date_time(self):
        dt = datetime.utcfromtimestamp(self.date)
        return dt.strftime("%d %b %y %H:%M:%S")

    def get_formated_date_time_min_day(self):
        dt = datetime.utcfromtimestamp(self.date)
        return dt.strftime("%d.%m")

    def __repr__(self):
        return "[" + self.email_from + ", " + self.from_name + ", " + self.subject + "]"
