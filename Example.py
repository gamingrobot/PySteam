from SteamAPI import *

steam = SteamAPI()

print steam.Authenticate("username", "password", "email_auth_code")

friends = steam.GetFriends()

#print steam.message("anotherSteamID", "Sent From Python")
