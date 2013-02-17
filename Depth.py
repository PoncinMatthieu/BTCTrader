

# store market depth
class Depth:
    def __init__(self, currency):
        self.currency = currency
        self.bids = []
        self.asks = []

    def GetDescription(self):
        desc = []
        desc.append("Depth:")
        desc.append("Currency: " + self.currency)
        desc.append("Bids: " + str(len(self.bids)))
        for b in self.bids:
            desc.append(str(b[0]) + " " + str(b[1]) + " " + str(b[2]))
        desc.append("Asks: " + str(len(self.asks)))
        for a in self.asks:
            desc.append(str(a[0]) + " " + str(a[1]) + " " + str(a[2]))
        return desc
