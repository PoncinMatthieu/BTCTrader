
# Store account informations
class Account:
    def __init__(self):
        self.btcAddress = ""
        self.tradeFee = 0
        self.wallets = {}

    def GetDescription(self):
        desc = []
        desc.append("Account:")
        desc.append("BtcAddress: ")
        desc.append(" - " + self.btcAddress)
        desc.append("TradeFee: " + str(self.tradeFee))
        desc.append("Wallets: ")
        for v in self.wallets.items():
            desc.append(" - " + v[0] + ": " + str(v[1]))
        return desc
