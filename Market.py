

import Globales
from Requester import Requester
from MtGoxRequester import MtGoxRequester
from BitcoinCentralRequester import BitcoinCentralRequester

# store every informations available on a market
# - apiName = the name of the api used
# - req = the requester corresponding to the api
# - account = the account informations
# - depth["currency"] = current depth of the market depending on the currency
class Market:
    def __init__(self, apiName, authId, authPass):
        self.apiName = apiName
        self.req = self.CreateRequester(authId, authPass)
        self.depth = {}

    def CreateRequester(self, authId, authPass):
        if (self.apiName == "mtgox"):
            return MtGoxRequester(authId, authPass)
        elif (self.apiName == "bitcoin-central"):
            return BitcoinCentralRequester(authId, authPass)
        raise Exception("Unknown Market.")

    def __str__(self):
        s = "Market: " + self.apiName + "\n"
        s += str(self.account)
        return s

    # Refresh informations that are not supposed to change often like the account balance
    def Refresh(self):
        self.account = self.req.GetAccount()

    # Update informations from the market
    def Update(self):
        self.req.UpdateDepth(self.depth)
