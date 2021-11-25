from views.email_create_detail_view import EmailCreateDetailView
from views.email_detail_view import EmailDetailView
from views.settings_detail_view import SettingsDetailView


class PageManager:
    pages = []

    def __init__(self):
        print("Page Manager")

    def load_pages(self):
        self.pages = []
        self.pages.append(SettingsDetailView([]))
        self.pages.append(EmailCreateDetailView())
        self.pages.append(EmailDetailView())

    def get_pages(self):
        return self.pages
