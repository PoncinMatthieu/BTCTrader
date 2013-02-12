
# Store account informations
class Account:
    btcAddress = ""
    tradeFee = 0
    wallets = {}

    def __str__(self):
        s = "BtcAddress: " + self.btcAddress + "\n"
        s += "TradeFee: " + str(self.tradeFee) + "\n"
        s += "Wallets: " + str(self.wallets) + "\n"
        return s
