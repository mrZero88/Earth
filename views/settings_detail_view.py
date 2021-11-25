import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


@Gtk.Template(filename="templates/xml/settingsPage.xml")
class SettingsDetailView(Gtk.Box):
    __gtype_name__ = "settingsPage"
    accounts = []
    parentWindow = None

    def __init__(self, accounts):
        super().__init__()
        self.accounts = accounts
        self.connect("realize", self._on_realize)
        self.init_controls()

    def init_controls(self):
        print("init")

    def _on_realize(self, widget):
        print("realize")
