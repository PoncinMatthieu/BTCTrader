#!/usr/bin/python

import sys
import getopt

import Globales

from Requester import Requester
from MtGoxRequester import MtGoxRequester
from BitcoinCentralRequester import BitcoinCentralRequester
from Market import Market

class BTCTrader:
    def ExitUsage(self, error=0, msg=""):
        if error != 0:
            print("Error: " + msg)
        print("usage: ./BTCTrader.py [OPTION] --markets=[MARKET_FILE_DESCRIPTION]")
        print("OPTION:")
        print("\t-h, --help: print usage.")
        print("\t-v, --verbose: verbose mode.")
        sys.exit(error)

    # constructor, here we take care of the arguments.
    # print the usage if something is wrong
    def __init__(self, argv):
        self.markets = {}
        try:
            opts, args = getopt.getopt(argv, "hv", ["help", "verbose", "markets="])
        except getopt.GetoptError:
            self.ExitUsage(1, "Bad arguments.")
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                self.ExitUsage()
            elif opt in ("-v", "--verbose"):
                Globales.verbose = 1
            elif opt == "--markets":
                self.marketFile = arg
                try:
                    f = open(self.marketFile, "r")
                    for line in f:
                        infos = line.partition(" ")
                        infos2 = infos[2].partition(" ")
                        self.markets[infos[0]] = Market(infos[0], infos2[0], infos2[2])
                except IOError as e:
                    self.ExitUsage(1, "Bad arguments. Failed to open the markets description file.")

    def Run(self):
        for m in self.markets.items():
            m[1].Init()
            print(m[1].account)


trader = BTCTrader(sys.argv[1:])
trader.Run()
