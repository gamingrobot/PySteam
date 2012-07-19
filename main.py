import pygtk
pygtk.require("2.0")
import gtk
from SteamAPI import *
from ChatBox import *


class PySteam:
    def __init__(self):
        filename = "PySteam.glade"
        self.builder = gtk.Builder()
        self.builder.add_from_file(filename)
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("windowMain")
        self.window.show()
        self.friendsView = self.builder.get_object("friendsView")

        self.AddListColumn("Name", 0)
        self.AddListColumn("steamid", 1)
        self.AddListColumn("Status", 2)
        self.friendsList = gtk.ListStore(str, str, str)
        self.friendsList.set_default_sort_func(None)
        self.friendsView.set_model(self.friendsList)

        self.login = self.builder.get_object("loginDlg")
        self.login.show()

        self.steam = SteamAPI()

    def AddListColumn(self, title, columnId):
        column = gtk.TreeViewColumn(title, gtk.CellRendererText(), text=columnId)
        column.set_resizable(True)
        self.friendsView.append_column(column)

    def userStatusToString(self, status):
        if status == UserStatus.Online:
            return "Online"
        elif status == UserStatus.Away:
            return "Away"
        elif status == UserStatus.Snooze:
            return "Snooze"
        elif status == UserStatus.Busy:
            return "Busy"
        elif status == UserStatus.Offline:
            return "Offline"

    def on_windowMain_destroy(self, widget):
        gtk.main_quit()

    def on_friendsView_button_press_event(self, widget, event):
        if event.type == gtk.gdk._2BUTTON_PRESS:
            pointer = event.window.get_pointer()
            selection = widget.get_path_at_pos(pointer[0], pointer[1])
            index = selection[0][0]
            ChatBox(self.steam, self.users[index])

    def on_login_clicked(self, widget):
        usernamef = self.builder.get_object("username")
        passwordf = self.builder.get_object("password")
        steamguardlb = self.builder.get_object("steamguardlb")
        steamguardf = self.builder.get_object("steamguard")
        username = usernamef.get_text()
        password = passwordf.get_text()

        status = self.steam.Authenticate(str(username), str(password), "")
        if status == LoginStatus.SteamGuard:
            steamguardlb.show()
            steamguardf.show()
            steamguard = steamguardf.get_text()
            status = self.steam.Authenticate(str(username), str(password), str(steamguard))

        if status == LoginStatus.LoginSuccessful:
            usernamef.set_text("")
            passwordf.set_text("")
            self.login.hide()
            poll = self.steam.Poll()
            friends = self.steam.GetFriends()
            self.users = self.steam.GetUserInfo(friends)
            #count = 0
            for user in self.users:
                self.friendsList.append([user.nickname, user.steamid, self.userStatusToString(user.status)])

if __name__ == '__main__':
    steam = PySteam()
    gtk.main()
