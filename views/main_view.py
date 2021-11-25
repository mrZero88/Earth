#!/usr/bin/env python3
import threading

import gi

from utils.asynk import Asynk
from viewmodels.main_view_model import MainViewModel
from utils.find_child import FindChild
from views.about_view import AboutView

gi.require_version("Gtk", "3.0")
gi.require_version('Notify', '0.7')
from gi.repository import Gtk, Notify


@Gtk.Template(filename="templates/xml/mainView.xml")
class MainView(Gtk.Window):
    __gtype_name__ = "window"

    # Main View Model
    mainViewModel = None
    selected_email_index = -1

    # Containers
    emailList = None
    stackDetail = None

    # Controls
    s1 = None
    btnReply = None
    btnReplyAll = None
    btnForward = None
    btnBold = None
    btnItalic = None
    btnUnderligned = None
    btnFormatLeft = None
    btnFormatCenter = None
    btnFormatRight = None
    btnFormatJustify = None
    btnInsertImage = None
    btnInsertAttachment = None
    btnSend = None
    bFormatEmail = None

    @Gtk.Template.Callback()
    def on_show(self, _):
        self.init()
        self.mainViewModel = MainViewModel(self, self.on_email_load)
        self.add_pages_to_stack()

    def on_email_load(self, email, error):
        er = self.mainViewModel.create_email_row(email)
        self.emailList.add(er)
        return False

    def init(self):
        self.init_controls()
        self.hide_all_controls()
        # Notification.show_notification("Mars", "Welcome back, " + self.user.first_name + "!",
        #                              "img/app_icon/mars64.png")

    def init_controls(self):
        self.s1 = FindChild.find_child(self, "s1")
        self.btnReply = FindChild.find_child(self, "btnReply")
        self.btnReplyAll = FindChild.find_child(self, "btnReplyAll")
        self.btnForward = FindChild.find_child(self, "btnForward")
        self.btnBold = FindChild.find_child(self, "btnBold")
        self.btnItalic = FindChild.find_child(self, "btnItalic")
        self.btnUnderligned = FindChild.find_child(self, "btnUnderligned")
        self.btnFormatLeft = FindChild.find_child(self, "btnFormatLeft")
        self.btnFormatCenter = FindChild.find_child(self, "btnFormatCenter")
        self.btnFormatRight = FindChild.find_child(self, "btnFormatRight")
        self.btnFormatJustify = FindChild.find_child(self, "btnFormatJustify")
        self.btnInsertImage = FindChild.find_child(self, "btnInsertImage")
        self.btnInsertAttachment = FindChild.find_child(self, "btnInsertAttachment")
        self.btnSend = FindChild.find_child(self, "btnSend")
        self.bFormatEmail = FindChild.find_child(self, "bFormatEmail")
        self.stackDetail = FindChild.find_child(self, "stackDetail")
        self.emailList = FindChild.find_child(self, "emailList")
        self.emailList.set_header_func(self.header_func, None, None)

    def add_pages_to_stack(self):
        for page in self.mainViewModel.get_pages():
            self.stackDetail.add(page)

    def header_func(self, row, before, user_data, other):
        if before is None:
            Gtk.ListBoxRow.set_header(row)
            return
        current = Gtk.ListBoxRow.get_header(row)
        if current is None:
            current = Gtk.Separator()
            current.set_orientation(orientation=Gtk.Orientation.HORIZONTAL)
            current.show()
            Gtk.ListBoxRow.set_header(row, current)

    def add_emails_to_ui(self, emails):
        email_rows = self.mainViewModel.get_email_rows()
        for i in range(0, len(emails)):
            self.emailList.add(email_rows[i])

    @Gtk.Template.Callback()
    def on_row_selected(self, *args):
        if args[1] is None:
            return
        self.show_email_controls()
        selected_index = args[1].get_index()
        self.mainViewModel.set_selected_index(selected_index)
        selected_email = self.mainViewModel.get_selected_email()
        email_detail_view = self.mainViewModel.get_page_by_name("detail")
        email_detail_view.bind_data(selected_email)
        self.stackDetail.set_visible_child(email_detail_view)
        self.selected_email_index = selected_index

    """
        On Pages Clicked
    """

    @Gtk.Template.Callback()
    def on_create_email_clicked(self, *args):
        self.show_new_email_controls()
        self.remove_stack_detail_selection()
        self.stackDetail.set_visible_child(self.mainViewModel.get_page_by_name("emailCreatePage"))

    @Gtk.Template.Callback()
    def on_settings_clicked(self, *args):
        self.show_settings_controls()
        self.remove_stack_detail_selection()
        self.stackDetail.set_visible_child(self.mainViewModel.get_page_by_name("settingsPage"))

    def remove_stack_detail_selection(self):
        self.emailList.unselect_all()
        self.selected_email_index = -1

    @Gtk.Template.Callback()
    def on_earth_clicked(self, element):
        about_view = AboutView(parent_window=self)
        about_view.show()

    @Gtk.Template.Callback()
    def on_key_pressed(self, widget, event):
        key_val = event.get_keyval()[1]
        # Space Key
        if key_val == 65535:
            self.open_delete_email_dialog()

    """
        Delete Email
    """

    def open_delete_email_dialog(self):
        dialog = Gtk.MessageDialog(transient_for=self, flags=Gtk.DialogFlags.MODAL,
                                   message_type=Gtk.MessageType.WARNING,
                                   buttons=Gtk.ButtonsType.YES_NO, text="Are you sure you want to delete this email?")
        response = dialog.run()
        if response == Gtk.ResponseType.YES:
            self.delete_email()
        dialog.destroy()

    def delete_email(self):
        email = self.mainViewModel.get_selected_email()
        email_page = self.mainViewModel.get_selected_email_page()
        email_listbox_row = self.emailList.get_children()[self.selected_email_index]
        self.selected_email_index = -1
        self.stackDetail.remove(email_page)
        self.emailList.remove(email_listbox_row)
        self.mainViewModel.emails.remove(email)
        self.mainViewModel.email_pages.remove(email_page)

    """
        Show/Hide Methods
    """

    def hide_all_controls(self):
        self.hide_email_controls()
        self.hide_settings_controls()
        self.hide_new_email_controls()

    def hide_email_controls(self):
        self.s1.set_visible(False)
        self.btnReply.set_visible(False)
        self.btnReplyAll.set_visible(False)
        self.btnForward.set_visible(False)

    def hide_settings_controls(self):
        print("Settings Controls Hidden")

    def hide_new_email_controls(self):
        self.btnSend.set_visible(False)
        self.bFormatEmail.set_visible(False)

    def show_email_controls(self):
        self.hide_all_controls()
        self.s1.set_visible(True)
        self.btnReply.set_visible(True)
        self.btnReplyAll.set_visible(True)
        self.btnForward.set_visible(True)

    def show_new_email_controls(self):
        self.hide_all_controls()
        self.btnSend.set_visible(True)
        self.bFormatEmail.set_visible(True)

    def show_settings_controls(self):
        self.hide_all_controls()
        print("Settings Controls Shown")

    @Gtk.Template.Callback()
    def on_destroy(self, *args):
        self.mainViewModel.close_db_connection()
        Notify.uninit()
        Gtk.main_quit()


window = MainView()
provider = Gtk.CssProvider()
provider.load_from_path("styles/scrolledWindow.css")
window.show()
Gtk.main()
