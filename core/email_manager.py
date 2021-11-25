import sqlite3
import threading
import time

from models.email import Email
from services.email_service import EmailService
from utils.encryption import Encryption
from gi.repository import GObject


class EmailManager:
    on_email_load = None

    def __init__(self, conn, account, on_email_load):
        self.conn = conn
        self.emails = []
        self.account = account
        self.on_email_load = on_email_load

    def load_emails(self):
        if self.exists_email():
            self.load_emails_from_database()
        else:
            self.load_emails_from_account(self.account, 100)
            self.insert_emails_in_database()

    def insert_emails_in_database(self):
        for email in self.emails:
            self.insert_email_in_database(email)

    def insert_email_in_database(self, email):
        cur = self.conn.cursor()
        cur.execute(
            "insert into emails ("
            "from_name,"
            "'from',"
            "'to',"
            "subject,"
            "file_path,"
            "cc,"
            "date,"
            "account_id"
            "'text'"
            ") values (?,?,?,?,?,?,?,?,?)",
            (
                email.from_name,
                email.email_from,
                email.to,
                email.subject,
                email.file_path,
                email.cc,
                email.date,
                email.account_id,
                email.text
            ))
        self.conn.commit()

    def load_emails_from_database(self):
        thread = threading.Thread(target=self.load_emails_from_database_async)
        thread.daemon = True
        thread.start()

    def load_emails_from_database_async(self):
        if not self.on_email_load:
            self.on_email_load = lambda r, e: None

        conn = sqlite3.connect("/home/danielcorreia/DataGripProjects/Earth/earth.sqlite")
        GObject.threads_init()
        error = None
        try:
            cur = conn.cursor()
            for row in cur.execute("select * from emails limit 100"):
                email = Email(
                    id=row[0],
                    from_name=row[1],
                    email_from=row[2],
                    to=row[3],
                    subject=row[4],
                    file_path=row[5],
                    cc=row[6],
                    date=row[7],
                    account_id=row[8],
                    text=row[9]
                )
                self.emails.append(email)
                GObject.idle_add(lambda: self.on_email_load(email, error))
                time.sleep(0.05)
            conn.close()
        except Exception as err:
            error = err
            conn.close()
            print(err)

    def load_emails_from_account(self, account, number_of_emails_to_read=3):
        es = EmailService(account, self.on_email_load, self.on_email_insert_in_database)
        pw = Encryption().decrypt_string(account.password)
        es.login(account.email, Encryption().decrypt_string(account.password))
        es.read_emails("INBOX", number_of_emails_to_read)

    def on_email_insert_in_database(self, email, error):
        self.emails.append(email)
        cur = self.conn.cursor()
        cur.execute(
            "insert into emails ("
            "from_name,"
            "'from',"
            "'to',"
            "subject,"
            "file_path,"
            "cc,"
            "date,"
            "account_id,"
            "'text'"
            ") values (?,?,?,?,?,?,?,?,?)",
            (
                email.from_name,
                email.email_from,
                email.to,
                email.subject,
                email.file_path,
                email.cc,
                email.date,
                email.account_id,
                email.text
            ))
        self.conn.commit()

    def add_email(self, email):
        self.emails.append(email)
        self.insert_email_in_database(email)

    def exists_email(self):
        try:
            cur = self.conn.cursor()
            row = cur.execute("select * from emails").fetchone()
            return True if row else False
        except Exception as e:
            print(e)
        return False

    def get_emails(self):
        return self.emails
