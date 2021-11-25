import gi

from utils.find_child import FindChild

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

gi.require_version("WebKit2", "4.0")
from gi.repository import WebKit2


@Gtk.Template(filename="templates/xml/emailDetail.xml")
class EmailDetailView(Gtk.Box):
    __gtype_name__ = "detail"
    email = None

    e_from = None
    e_to = None
    e_subject = None
    webkit = None

    def __init__(self):
        super().__init__()
        self.init_controls()

    def init_controls(self):
        self.e_from = FindChild.find_child(self, "eFrom")
        self.e_to = FindChild.find_child(self, "eTo")
        self.e_subject = FindChild.find_child(self, "eSubject")
        self.webkit = FindChild.find_child(self, "webkit")

    def bind_data(self, email):
        self.e_from.set_text(email.email_from)
        self.e_to.set_text(email.to)
        self.e_subject.set_text(email.subject)

        a = WebKit2.WebView()

        content = ""
        with open(email.file_path) as f:
            content = f.read()

        # self.webkit.set_tls_errors_policy(WebKit2.TLSErrorsPolicy.IGNORE)
        self.webkit.load_html(content, "file://" + email.file_path)
