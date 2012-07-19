import pygtk
pygtk.require("2.0")
import gtk
from SteamAPI import *


class ChatBox:
    def __init__(self, steam, user):
        self.steam = steam
        self.user = user
        filename = "ChatBox.glade"
        self.builder = gtk.Builder()
        self.builder.add_from_file(filename)
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("chat")
        self.window.show()

        self.builder.get_object("chat_name").set_text(user.nickname)

    def on_chat_message_activate(self, widget):
        self.steam.SendMessage(self.user, widget.get_text())
