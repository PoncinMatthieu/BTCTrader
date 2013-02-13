

# store market depth
class Depth:
    currency = ""
    bids = []
    asks = []

    def __init__(self, currency):
        self.currency = currency

    def __str__(self):
        s = "Depth:\n"
        s += "Currency: " + self.currency + "\n"
        s += "Bids: " + str(len(self.bids)) + "\n"
        for b in self.bids:
            s += str(b[0]) + " " + str(b[1]) + " " + str(b[2]) + "\n"
        s += "Asks: " + str(len(self.asks)) + "\n"
        for a in self.asks:
            s += str(a[0]) + " " + str(a[1]) + " " + str(a[2]) + "\n"
        return s
