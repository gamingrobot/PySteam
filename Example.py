from SteamAPI import *

steam = SteamAPI()

username = raw_input("Username: ")
password = raw_input("Password: ")

status = steam.Authenticate(str(username), str(password), "")
if status == LoginStatus.SteamGuard:
    steamguard = raw_input("SteamGuard Code: ")
    status = steam.Authenticate(str(username), str(password), str(steamguard))

if status == LoginStatus.LoginSuccessful:
    friends = steam.GetFriends()
    users = steam.GetUserInfo(friends)
    count = 0
    for user in users:
        print str(count) + ": Nick: " + str(user.nickname) + " Steamid: " + str(user.steamid)
        count = count + 1

    message = raw_input("Who do you want to msg?: ")

    steam.SendMessage(users[message], "Python Rocks")

else:
    print "Failed to login!"
