import httplib
import urllib
import json


class LoginStatus:
    LoginFailed, LoginSuccessful, SteamGuard = range(3)


class UserStatus:
    Offline = 0
    Online = 1
    Busy = 2
    Away = 3
    Snooze = 4


class ProfileVisibility:
    Private = 1
    Public = 3
    FriendsOnly = 8


class AvatarSize:
    Small, Medium, Large = range(3)


class UpdateType:
    UserUpdate, Message, Emote, TypingNotification = range(4)


class Friend:
    steamid = None
    blocked = None
    friendSince = None


class User:
    steamid = None
    profileVisibility = None
    profileState = None
    nickname = None
    lastLogoff = None
    profileUrl = None
    avatarUrl = None
    status = None
    realName = None
    primaryGroupId = None
    joinDate = None
    locationCountryCode = None
    locationStateCode = None
    locationCityCode = None


class Group:
    steamid = None
    inviteonly = None


class GroupInfo:
    steamid = None
    creationDate = None
    name = None
    headline = None
    summary = None
    abbreviation = None
    profileUrl = None
    avatarUrl = None
    locationCountryCode = None
    locationStateCode = None
    locationCityId = None
    favoriteAppId = None
    members = None
    usersOnline = None
    usersInChat = None
    usersInGame = None
    owner = None


class Update:
    timestamp = None
    origin = None
    localMessage = None
    utype = None
    message = None
    status = None
    nick = None


class ServerInfo:
    serverTime = None
    serverTimeString = None


class SteamAPI:
    def __init__(self):
        self.oauth_client_id = "DE45CD61"

    def Authenticate(self, username, password, email_auth_code):
        response = self.steamRequest("ISteamOAuth2", "GetTokenWithCredentials",
                                {'client_id': self.oauth_client_id,
                 'grant_type': 'password',
                 'username': username,
                 'password': password,
                 'x_emailauthcode': email_auth_code,
                 'scope': 'read_profile write_profile read_client write_client'}, True)
        if response != None:
            if 'access_token' in response:
                self.accessToken = response['access_token']
                self.steamId = response['x_steamid']
                loginbool = self.__login()
                if loginbool:
                    return LoginStatus.LoginSuccessful
                else:
                    return LoginStatus.LoginFailed
            elif response['x_errorcode'] == "steamguard_code_required":
                return LoginStatus.SteamGuard
            else:
                return LoginStatus.LoginFailed
        else:
            return LoginStatus.LoginFailed

    def AuthenticateWithAccessToken(self, accessToken):
        self.accessToken = accessToken
        loginbool = self.__login()
        if loginbool:
            return LoginStatus.LoginSuccessful
        else:
            return LoginStatus.LoginFailed

    def GetFriends(self, steamid=None):
        if steamid == None:
            steamid = self.steamId
        response = self.steamRequest("ISteamUserOAuth", "GetFriendList", {"access_token": self.accessToken, "steamid": steamid})
        if response != None:
            if 'friends' in response:
                friends = []
                for friend in response['friends']:
                    f = Friend()
                    f.steamid = str(friend['steamid']) if 'steamid' in friend else ""
                    f.blocked = str(friend['relationship']) == "ignored" if 'relationship' in friend else ""
                    f.friendSince = friend['friend_since'] if 'friend_since' in friend else ""
                    friends.append(f)
                return friends
            else:
                return None
        else:
            return None

    def GetUserInfo(self, data):
        #list of either steamids, or list of friends
        if type(data) == list:
            if len(data) > 0:
                #its a list of friends
                if isinstance(data[0], Friend):
                    steamids = []
                    for f in data:
                        steamids.append(f.steamid)
                    return self.__getSteamIDsUserInfo(steamids)
                #its a list of steamids
                elif type(data[0]) == str or type(data[0]) == int:
                    return self.__getSteamIDsUserInfo(data)
                #its a list of something else
                else:
                    return None
            else:
                return None
        #its a steamid
        elif type(data) == str or type(data) == int:
            return self.__getSteamIDsUserInfo([str(data)])
        #just one friend
        elif isinstance(data, Friend):
            return self.__getSteamIDsUserInfo([data.steamid])
        #wtf did you pass
        else:
            return None

    def __getSteamIDsUserInfo(self, steamids):
        #TODO: fix 100 steam id limit
        steamidString = ', '.join(steamids)
        response = self.steamRequest("ISteamUserOAuth", "GetUserSummaries", {"access_token": self.accessToken, "steamids": steamidString})
        if response != None:
            if 'players' in response:
                users = []
                for info in response['players']:
                    user = User()
                    user.steamid = str(info['steamid']) if 'steamid' in info else ""
                    user.profileVisibility = info['communityvisibilitystate'] if 'communityvisibilitystate' in info else ""
                    user.profileState = int(info['profilestate']) if 'profilestate' in info else ""
                    user.nickname = info['personaname'] if 'personaname' in info else ""
                    user.lastLogoff = info['lastlogoff'] if 'lastlogoff' in info else ""
                    user.profileUrl = str(info['profileurl']) if 'profileurl' in info else ""
                    user.status = info['personastate'] if 'personastate' in info else ""

                    if 'avatar' in info:
                        user.avatarUrl = str(info['avatar'])
                        #lop off the .jpg
                        user.avatarUrl = user.avatarUrl[:-4]
                    else:
                        user.avatarUrl = ""

                    user.joinDate = info['timecreated'] if 'timecreated' in info else ""
                    user.primaryGroupId = info['primaryclanid'] if 'primaryclanid' in info else ""
                    user.realName = info['realname'] if 'realname' in info else ""
                    user.locationCountryCode = str(info['loccountrycode']) if 'loccountrycode' in info else ""
                    user.locationStateCode = str(info['locstatecode']) if 'locstatecode' in info else ""
                    user.locationCityCode = str(info['loccityid']) if 'loccityid' in info else ""

                    users.append(user)

                #TODO: do check here for over 100 steamids, then recall function
                if len(steamids) > 100:
                    print "OVER 100 STEAM IDS"
                return users
            else:
                return None
        else:
            return None

    def GetUserAvatar(self, user, size=AvatarSize.Small):
        if len(user.avatarUrl) == 0:
            return None
        if size == AvatarSize.Small:
            return user.avatarUrl + ".jpg"
        elif size == AvatarSize.Medium:
            return user.avatarUrl + "_medium.jpg"
        else:
            return user.avatarUrl + "_full.jpg"

    def GetGroupAvatar(self, group, size=AvatarSize.Small):
        user = User()
        user.avatarUrl = group.avatarUrl
        return self.GetUserAvatar(user, size)

    def GetGroups(self, steamid=None):
        if steamid == None:
            steamid = self.steamId
        pass

    def GetGroupInfo(self, data):
        #check if list of steamids, or 1 steamid, or list of Groups
        pass

    def SendTypingNotification(self, data):
        #its a user class
        if isinstance(data, User):
            steamid = data.steamid
        #its a steamid
        elif type(data) == str or type(data) == int:
            steamid = str(data)
        #no idea what it is
        else:
            return False
        response = self.steamRequest("ISteamWebUserPresenceOAuth", "Message", {"access_token": self.accessToken, "umqid": self.umqid, "type": "typing", "steamid_dst": steamid}, True)
        if response != None:
            if 'error' in response:
                return str(response['error']) == "OK"
        else:
            return False

    def SendMessage(self, data, message):
        #its a user class
        if isinstance(data, User):
            steamid = data.steamid
        #its a steamid
        elif isinstance(data, (str, int, float)):
            steamid = str(data)
        #no idea what it is
        else:
            return False
        response = self.steamRequest("ISteamWebUserPresenceOAuth", "Message", {"access_token": self.accessToken, "umqid": self.umqid, "type": "saytext", "text": str(message), "steamid_dst": steamid}, True)
        print response
        if response != None:
            if 'error' in response:
                return str(response['error']) == "OK"
        else:
            return False

    def Poll(self):
        response = self.steamRequest("ISteamWebUserPresenceOAuth", "Poll", {"access_token": self.accessToken, "umqid": self.umqid, "message": self.message}, True)
        if response != None:
            if 'error' in response:
                if str(response['error']) == "OK":
                    self.message = int(response['messagelast'])
                    updates = []
                    for info in response['messages']:
                        update = Update()

                        update.timestamp = info["timestamp"] if 'timestamp' in info else ""
                        update.origin = str(info["steamid_from"]) if 'steamid_from' in info else ""

                        ut = str(info["type"]) if 'type' in info else ""
                        if ut == "saytext" or ut == "my_saytext" or ut == "emote":
                            update.utype = UpdateType.Emote if ut == "emote" else UpdateType.Message
                            update.message = str(info["text"]) if 'text' in info else ""
                            update.localMessage = ut == "my_saytext"
                        elif ut == "typing":
                            update.utype = UpdateType.TypingNotification
                            update.message = str(info["text"]) if 'text' in info else ""  # Not sure if this is useful
                        elif ut == "personastate":
                            update.utype = UpdateType.UserUpdate
                            update.status = int(info["persona_state"]) if 'persona_state' in info else ""
                            update.nick = str(info["persona_name"]) if 'persona_name' in info else ""
                        else:
                            continue

                        updates.append(update)
                    return updates
                else:
                    return None
            else:
                return None
        else:
            return None

    def GetServerInfo(self):
        response = self.steamRequest("ISteamWebAPIUtil", "GetServerInfo", {})
        if response != None:
            if 'servertime' in response:
                info = ServerInfo()
                info.serverTime = response['servertime'] if 'servertime' in response else ""
                info.serverTimeString = str(response['servertimestring']) if 'servertimestring' in response else ""
                return info
            else:
                return None
        else:
            return None

    def __login(self):
        response = self.steamRequest("ISteamWebUserPresenceOAuth", "Logon", {"access_token": self.accessToken}, True)
        if response != None:
            if 'umqid' in response:
                self.steamid = response['steamid']
                self.umqid = response['umqid']
                self.message = response['message']
                return True
            else:
                return False
        else:
            return False

    def steamRequest(self, api, method, data, post=False):
        params = urllib.urlencode(data)
        headers = {"Content-type": "application/x-www-form-urlencoded", "User-Agent": "Steam 1291812 / iPhone", "Accept-Language": "en-us", "Accept-Encoding": "gzip, deflate", "Accept": "*/*"}
        c = httplib.HTTPSConnection("api.steampowered.com:443")
        #c.set_debuglevel(1)
        if post:
            c.request("POST", "/" + api + "/" + method + "/v0001", params, headers)
        else:
            c.request("GET", "/" + api + "/" + method + "/v0001?" + params, None, headers)
        response = c.getresponse()
        if response.status == 200:
            data = response.read()
            #print data
            try:
                parjson = json.loads(data)
            except:
                return None
            if parjson != None:
                return parjson
            else:
                return {}
        else:
            return None
