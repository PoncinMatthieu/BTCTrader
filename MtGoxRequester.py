
import time
from hashlib import sha512
from hmac import HMAC
import base64
import urllib

from Requester import Requester
from Account import Account

# Manage every requests to MtGox API
class MtGoxRequester(Requester):
    def __init__(self, authId, authPass):
        Requester.__init__(self, "https://mtgox.com/api/1")
        self._authKey = authId
        self._authSecret = base64.b64decode(authPass.encode())

    def GetNonce(self):
        return int(time.time()*100000)

    def SignData(self, secret, data):
        return base64.b64encode(HMAC(secret, data.encode(), sha512).digest())

    def BuildQuery(self, req={}):
        req["nonce"] = self.GetNonce()
        postData = urllib.parse.urlencode(req)
        headers = {}
        headers["User-Agent"] = "GoxApi"
        headers["Rest-Key"] = self._authKey
        headers["Rest-Sign"] = self.SignData(self._authSecret, postData)
        return (postData, headers)

    def Perform(self, url, args):
        res = Requester.Perform(self, url, args)
        if res["result"] != "success":
            raise Exception("Request failed.")
        return res

    def GetAccount(self):
        # get account infos
        res = self.Perform("/generic/private/info", {})
        result = res["return"]
        a = Account()
        a.tradeFee = result["Trade_Fee"]
        a.wallets["BTC"] = result["Wallets"]["BTC"]["Balance"]["value"]
        a.wallets["EUR"] = result["Wallets"]["EUR"]["Balance"]["value"]
        # get btc address
        res = self.Perform("/generic/bitcoin/address", {})
        #a.address = result
        return a
