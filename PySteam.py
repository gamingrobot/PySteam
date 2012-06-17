import httplib
import urllib
import json


class PySteam:
    def __init__(self, hash):
        self.username = hash['username']
        self.password = hash['password']
        self.email_auth_code = hash['email_auth_code']
        self.oauth_client_id = "DE45CD61"

    def request(self, api, method, data, post=False):
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

    def request_auth(self, api, method, data={}, post=False):
        data['access_token'] = self.access_token
        data['steamid'] = self.steam_id
        return self.request(api, method, data, post)

    def request_umq(self, api, method, data={}, post=False):
        data['access_token'] = self.access_token
        data['umqid'] = 5
        return self.request(api, method, data, post)

    def authenticate(self):
        login = self.request("ISteamOAuth2", "GetTokenWithCredentials",
                                {'client_id': self.oauth_client_id,
                 'grant_type': 'password',
                 'username': self.username,
                 'password': self.password,
                 'x_emailauthcode': self.email_auth_code,
                 'scope': 'read_profile write_profile read_client write_client'}, True)
        self.access_token = login['access_token']
        #self.webcookie = login['x_webcookie']
        self.steam_id = login['x_steamid']

    def friends(self):
        return self.request_auth("ISteamUserOAuth", "GetFriendList", {"access_token": self.access_token, "steamid": self.steam_id})

    def chat_login(self):
        return self.request_umq("ISteamWebUserPresenceOAuth", "Logon", {}, True)

    def message(self, recipient, message):
        return self.request_umq("ISteamWebUserPresenceOAuth", "Message",
                {'type': 'saytext', 'steamid_dst': recipient, 'text': message}, True)
