import httplib
import urllib
import json


class SteamAPI:
    def __init__(self):
        self.oauth_client_id = "DE45CD61"

    def Authenticate(self, username, password, email_auth_code):
        auth = self.steamRequest("ISteamOAuth2", "GetTokenWithCredentials",
                                {'client_id': self.oauth_client_id,
                 'grant_type': 'password',
                 'username': username,
                 'password': password,
                 'x_emailauthcode': email_auth_code,
                 'scope': 'read_profile write_profile read_client write_client'}, True)
        print auth
        self.accessToken = auth['access_token']
        #self.webcookie = login['x_webcookie']
        self.steamId = auth['x_steamid']
        return self.login()

    def AuthenticateAccessToken(self, accessToken):
        self.accessToken = accessToken
        return self.login()

    def GetFriends(self, steamid=None):
        if steamid == None:
            steamid = self.steamId
        return self.steamRequest("ISteamUserOAuth", "GetFriendList", {"access_token": self.accessToken, "steamid": steamid})

    def GetUserInfo(self, steamids):
        pass

    def GetFriendsUserInfo(self, friends):
        pass

    def GetOneUserInfo(self, steamid=None):
        if steamid == None:
            steamid = self.steamId
        pass

    def GetUserAvatar(self, user, size):
        pass

    def GetGroupAvatar(self, group, size):
        pass

    def GetGroups(self, steamid=None):
        if steamid == None:
            steamid = self.steamId
        pass

    def GetGroupInfo(self, steamids):
        pass

    def GetGroupsInfo(self, groups):
        pass

    def GetOneGroupInfo(self, steamid=None):
        if steamid == None:
            steamid = self.steamId
        pass

    def SendTypingNotification(self, user):
        pass

    def SendMessage(self, user, message):
        pass

    def SendSteamidMessage(self, user, message):
        pass

    def Poll(self):
        pass

    def GetServerInfo(self):
        pass

    def message(self, recipient, message):
        return self.steamRequest("ISteamWebUserPresenceOAuth", "Message",
                {'type': 'saytext', 'steamid_dst': recipient, 'text': message, "access_token": self.accessToken, "umqid": 5}, True)

    def login(self):
        return self.steamRequest("ISteamWebUserPresenceOAuth", "Logon", {"access_token": self.accessToken, "umqid": 5}, True)

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
            #print response.status, response.reason
            data = response.read()
            #print data
            #fix so none is status good
            return json.loads(data)
        else:
            return 0


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
