import gi

from utils.find_child import FindChild

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

gi.require_version('WebKit2', '4.0')
from gi.repository.WebKit2 import WebView


@Gtk.Template(filename="templates/xml/emailCreateDetail.xml")
class EmailCreateDetailView(Gtk.Box):
    __gtype_name__ = "emailCreatePage"
    email = None
    parentWindow = None

    e_from = None
    e_to = None
    e_subject = None
    tv_message = None

    def __init__(self):
        super().__init__()
        self.init_controls()

    def init_controls(self):
        self.e_from = FindChild.find_child(self, "eFrom")
        self.e_to = FindChild.find_child(self, "eTo")
        self.e_subject = FindChild.find_child(self, "eSubject")
        self.tv_message = FindChild.find_child(self, "tvMessage")

    def bind_data(self):
        self.e_from.set_text(self.email.email_from_name)
        self.e_to.set_text(self.email.email_to)
        self.e_subject.set_text(self.email.email_subject)
