from SteamAPI import *

steam = SteamAPI()

username = raw_input("Username: ")
password = raw_input("Password: ")

status = steam.Authenticate(str(username), str(password), "")
if status == LoginStatus.SteamGuard:
    steamguard = raw_input("SteamGuard Code: ")
    status = steam.Authenticate(str(username), str(password), str(steamguard))

if status == LoginStatus.LoginSuccessful:
    poll = steam.Poll()
    friends = steam.GetFriends()
    users = steam.GetUserInfo(friends)
    count = 0
    for user in users:
        print str(count) + ": Nick: " + user.nickname + " Steamid: " + str(user.steamid)
        count = count + 1

    msgid = raw_input("Who do you want to msg?: ")
    msg = raw_input("Message: ")

    steam.SendMessage(users[int(msgid)], msg)

else:
    print "Failed to login!"
