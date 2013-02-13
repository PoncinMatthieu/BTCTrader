
import time

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
        startTime = time.time()
        elapsedTime = 0
        first = 1
        # for now we simply update informations every 60 seconds and process the informations
        # we don't want to block the thread for too long, so we sleep only for 1 second
        while Globales.stopBot == 0:
            try:
                if elapsedTime > 60 or first == 1:
                    first = 0
                    startTime = time.time()
                    self.Update()
                    self.Process()
                time.sleep(1)
                elapsedTime = time.time() - startTime
            except:
                print("Error in market: " + self.apiName)
                print(traceback.format_exc())

    # for now we only print the market infos
    def Process(self):
        print(self)
