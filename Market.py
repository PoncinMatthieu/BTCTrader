

import Globales
from Requester import Requester
from MtGoxRequester import MtGoxRequester
from BitcoinCentralRequester import BitcoinCentralRequester

class Market:
    def __init__(self, apiName, authId, authPass):
        self.apiName = apiName
        self.req = self.CreateRequester(authId, authPass)

    def CreateRequester(self, authId, authPass):
        if (self.apiName == "mtgox"):
            return MtGoxRequester(authId, authPass)
        elif (self.apiName == "bitcoin-central"):
            return BitcoinCentralRequester(authId, authPass)
        raise Exception("Unknown Market.")

    def Init(self):
        self.account = self.req.GetAccount()
