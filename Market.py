

import Globales
from Requester import Requester
from MtGoxRequester import MtGoxRequester
from BitcoinCentralRequester import BitcoinCentralRequester
from Engine import Engine
from Clock import Clock

# store every informations available on a market
# - apiName = the name of the api used
# - req = the requester corresponding to the api
# - account = the account informations
# - depth["currency"] = current depth of the market depending on the currency
class Market(Engine):
    def __init__(self, apiName, authId, authPass):
        Engine.__init__(self, 1) # refresh rate of 1 second. In the futur with the websockets we will probably put 0 and use some kind of select
        self.apiName = apiName
        self.req = self.CreateRequester(authId, authPass)
        self.depth = {}
        self.clock = Clock()
        self.first = 1

    def CreateRequester(self, authId, authPass):
        if (self.apiName == "mtgox"):
            return MtGoxRequester(authId, authPass)
        elif (self.apiName == "bitcoin-central"):
            return BitcoinCentralRequester(authId, authPass)
        raise Exception("Unknown Market.")

    def __str__(self):
        s = "Market: " + self.apiName + "\n"
        s += str(self.account)
        for d in self.depth.items():
            s += str(d[1])
        return s

    # Refresh personal informations,
    # those informations are not supposed to change if the bot does not perform any action
    def Refresh(self):
        self.account = self.req.GetAccount()

    # Update informations from the market
    def Update(self):
        self.req.UpdateDepth(self.depth)

    # infinit loop running the market trading algorithm
    def Run(self):
        self.Refresh()
        Engine.Run(self)

    # for now we only update and print the market infos every 60 seconds
    def Execute(self, elapsedTime):
        if self.clock.ElapsedTime() > 60 or self.first == 1:
            self.first = 0
            self.Update()
            self.clock.Reset()
            print(self)
