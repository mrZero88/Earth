import gi

from models.config import Config

gi.require_version("Gtk", "3.0")
gi.require_version('Notify', '0.7')
from gi.repository import Gtk, GdkPixbuf

"""
This class displays the about view.
"""


class AboutView(Gtk.AboutDialog):
    def __init__(self, parent_window):
        super().__init__()
        config = Config.get()
        pixbuf = GdkPixbuf.Pixbuf.new_from_file("img/app_icon/earth256.png")
        self.set_transient_for(parent_window)
        self.set_logo(pixbuf)
        self.set_program_name(config.app_name)
        self.set_comments(config.app_description)
        self.set_authors(config.authors)
        self.set_artists(config.artists)
        self.set_website_label(config.website)
        self.set_website(config.website)
        self.set_version(config.version)
        self.set_license(config.license)
        self.set_wrap_license(True)
        self.set_copyright(config.copyright)
        self.set_modal(True)
