import gi

from utils.find_child import FindChild

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


@Gtk.Template(filename="templates/xml/emailRow.xml")
class EmailRowView(Gtk.Box):
    __gtype_name__ = "row"
    lbl_from = None
    lbl_subject = None
    lbl_message = None
    lbl_date_time = None

    def __init__(self, email):
        super().__init__()
        self.email = email
        self.init_controls()
        self.bind_data()

    def init_controls(self):
        self.lbl_from = FindChild.find_child(self, "lblFromName")
        self.lbl_subject = FindChild.find_child(self, "lblSubject")
        self.lbl_message = FindChild.find_child(self, "lblMessage")
        self.lbl_date_time = FindChild.find_child(self, "lblDateTime")

    def bind_data(self):
        self.lbl_from.set_label(self.email.from_name)
        self.lbl_subject.set_label(self.email.subject)
        # self.lbl_message.set_label(self.email.email_message.replace("\n", ""))
        self.lbl_date_time.set_label(self.email.get_formated_date_time_min_day())
