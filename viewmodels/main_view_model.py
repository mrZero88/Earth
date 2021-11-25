import sqlite3
import sys

from core.account_manager import AccountManager
from views.email_row_view import EmailRowView
from core.page_manager import PageManager
from core.user_manager import UserManager
from core.email_manager import EmailManager


class MainViewModel:
    PROJECT_ROOT = sys.path[1]

    um = None
    pm = None
    am = None
    em = None

    # Parent Window
    window = None
    # List of email accounts of the app
    accounts = []
    # List of pages of the app
    pages = []
    # List of emails of the app
    emails = []
    # Selected Email
    selected_email = None
    # List of email pages
    email_pages = []
    # Selected Page
    selected_page = None
    # List of email rows
    email_rows = []
    # Selected email row
    selected_email_row = None
    # User
    user = None
    # Database
    conn = None

    def __init__(self, window, on_email_load):
        self.window = window
        self.on_email_load = on_email_load
        self.conn = sqlite3.connect("/home/danielcorreia/DataGripProjects/Earth/earth.sqlite")
        self.load_user()
        self.load_pages()
        self.load_accounts()
        self.load_emails()

    def load_user(self):
        self.um = UserManager(self.conn)
        self.um.load_user()
        self.user = self.um.get_user()

    def load_pages(self):
        self.pm = PageManager()
        self.pm.load_pages()
        self.pages = self.pm.get_pages()

    def load_accounts(self):
        self.am = AccountManager(self.conn)
        self.am.load_accounts()
        self.accounts = self.am.get_accounts()

    def load_emails(self):
        self.em = EmailManager(self.conn, self.am.get_default_account(), self.on_email_load)
        self.em.load_emails()
        self.emails = self.em.get_emails()

    def create_email_rows(self):
        for email in self.emails:
            email_row = EmailRowView(email)
            self.email_rows.append(email_row)

    def create_email_row(self, email):
        email_row = EmailRowView(email)
        self.email_rows.append(email_row)
        return email_row

    def set_selected_index(self, index):
        self.selected_email = self.emails[index]
        self.selected_email_row = self.email_rows[index]

    def get_page_by_name(self, page_name):
        for page in self.pages:
            if page.__gtype_name__ == page_name:
                return page
        return None

    def get_emails(self):
        return self.emails

    def get_pages(self):
        return self.pages

    def get_email_rows(self):
        return self.email_rows

    def get_email_pages(self):
        return self.email_pages

    def get_selected_email_page(self):
        return self.selected_page

    def get_selected_email(self):
        return self.selected_email

    def get_selected_email_row(self):
        return self.selected_email_row

    def close_db_connection(self):
        self.conn.close()
