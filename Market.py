

import Globales
from Requester import Requester
from MtGoxRequester import MtGoxRequester
from BitcoinCentralRequester import BitcoinCentralRequester
from Engine import Engine
from Clock import Clock
from Account import Account

# store every informations available on a market
# - apiName = the name of the api used
# - req = the requester corresponding to the api
# - account = the account informations
# - depth["currency"] = current depth of the market depending on the currency
class Market(Engine):
    def __init__(self, btcTrader, apiName, authId, authPass):
        Engine.__init__(self, apiName, btcTrader, 1) # refresh rate of 1 second. In the futur with the websockets we will probably put 0 and use some kind of select
        self.req = self.CreateRequester(authId, authPass)
        self.depth = {}
        self.clock = Clock()
        self.first = 1
        self.account = Account()

    def CreateRequester(self, authId, authPass):
        if (self.engineName == "mtgox"):
            return MtGoxRequester(authId, authPass)
        elif (self.engineName == "bitcoin-central"):
            return BitcoinCentralRequester(authId, authPass)
        raise Exception("Unknown Market.")

    def GetDescription(self):
        desc = Engine.GetDescription(self)
        desc.extend(self.account.GetDescription())
        return desc

    # Refresh personal informations,
    # those informations are not supposed to change if the bot does not perform any action
    def Refresh(self):
        self.account = self.req.GetAccount()
        self.PushMsg("account updated.")

    # Update informations from the market
    def Update(self):
        self.req.UpdateDepth(self.depth)
        self.PushMsg("Depth updated.")

    def Initialize(self):
        self.Refresh()

    # for now we only update the market infos every 60 seconds
    def Execute(self, elapsedTime):
        if self.clock.ElapsedTime() > 60 or self.first == 1:
            self.first = 0
            self.Update()
            self.clock.Reset()

    def CleanUp(self):
        i = 0 # do nothing
