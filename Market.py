

import Globales
from Requester import Requester
from MtGoxRequester import MtGoxRequester

class Market:
    def __init__(self, apiName, authId, authPass):
        self.apiName = apiName
        req = self.CreateRequester(authId, authPass)
        account = req.GetAccount()
        print(account)

    def CreateRequester(self, authId, authPass):
        if (self.apiName == "mtgox"):
            return MtGoxRequester(authId, authPass)
        elif (self.apiName == "bitcoin-central"):
            print("please implement me :'(")
        raise Exception("Unknown Market.")

