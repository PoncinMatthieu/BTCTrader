
import time
from hashlib import sha512
from hmac import HMAC
import base64
import urllib

from Requester import Requester
from Account import Account
from Depth import Depth

# Manage every requests to MtGox API
class MtGoxRequester(Requester):
    def __init__(self, authId, authPass):
        Requester.__init__(self, "https://mtgox.com/api/1")
        self._authKey = authId
        self._authSecret = base64.b64decode(authPass.encode())
        # for now, we will manage only EUR.
        #self._availableCurrencies = {"USD", "EUR", "JPY", "CAD", "GBP", "CHF", "RUB", "AUD", "SEK", "DKK", "HKD", "PLN", "CNY", "SGD", "THB", "NZD", "NOK"}
        self._availableCurrencies = {"EUR"}

    def GetNonce(self):
        return int(time.time()*100000)

    def SignData(self, secret, data):
        return base64.b64encode(HMAC(secret, data.encode(), sha512).digest())

    def BuildQuery(self, req={}, withAuth=0):
        req["nonce"] = self.GetNonce()
        postData = urllib.parse.urlencode(req)
        headers = {}
        headers["User-Agent"] = "GoxApi"
        if withAuth == 1:
            headers["Rest-Key"] = self._authKey
            headers["Rest-Sign"] = self.SignData(self._authSecret, postData)
        return (postData, headers)

    def Perform(self, url, args, withAuth):
        res = Requester.Perform(self, url, args, withAuth)
        if res["result"] != "success":
            raise Exception("Request failed.")
        return res

    def GetAccount(self):
        # get account infos
        res = self.Perform("/generic/private/info", {}, 1)
        result = res["return"]
        a = Account()
        a.tradeFee = result["Trade_Fee"]
        a.wallets["BTC"] = result["Wallets"]["BTC"]["Balance"]["value"]
        a.wallets["EUR"] = result["Wallets"]["EUR"]["Balance"]["value"]
        # get btc address
        res = self.Perform("/generic/bitcoin/address", {}, 1)
        a.btcAddress = res["return"]["addr"];
        return a

    def UpdateDepth(self, depth):
        for currency in self._availableCurrencies:
            res = self.Perform("/BTC" + currency + "/depth", {}, 0)
            res = res["return"]
            bids = res["bids"]
            asks = res["asks"]
            currentDepth = depth[currency] = Depth(currency)
            for bid in bids:
                currentDepth.bids.append([bid["stamp"], bid["amount"], bid["price"]])
            for ask in asks:
                currentDepth.asks.append([ask["stamp"], ask["amount"], ask["price"]])


