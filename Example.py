from SteamAPI import *

steam = SteamAPI()

print Group.steamid

print steam.Authenticate("username", "password", "email_auth_code")
print steam.chat_login()

print steam.friends()

print steam.message("anotherSteamID", "Sent From Python")
