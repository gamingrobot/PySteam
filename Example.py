from PySteam import *

steam = PySteam({"username": "username",
                 "password": "password",
                 "email_auth_code": ""})  # Run once to get auth code

print steam.authenticate()
print steam.chat_login()

print steam.friends()

print steam.message("anotherSteamID", "Sent From Python")
