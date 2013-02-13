#!/usr/bin/python

import sys
import getopt
import traceback
import threading

import Globales

from Requester import Requester
from MtGoxRequester import MtGoxRequester
from BitcoinCentralRequester import BitcoinCentralRequester
from Market import Market

class BTCTrader:
    def ExitUsage(self, error=0, msg=""):
        if error != 0:
            print("Error: " + msg)
        print("usage: ./BTCTrader.py [OPTION] --markets=[MARKET_FILE_DESCRIPTION] [--testmode=[FILE]]")
        print("OPTION:")
        print("\t-h, --help: print usage.")
        print("\t-v, --verbose: verbose mode.")
        sys.exit(error)

    # constructor, here we take care of the arguments.
    # print the usage if something is wrong
    def __init__(self, argv):
        self.markets = {}
        marketFileDefined = 0
        try:
            opts, args = getopt.getopt(argv, "hv", ["help", "verbose", "markets=", "testmode="])
        except getopt.GetoptError:
            self.ExitUsage(1, "Bad arguments.")
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                self.ExitUsage()
            elif opt in ("-v", "--verbose"):
                Globales.verbose = 1
            elif opt == "--markets":
                marketFileDefined = 1
                self.marketFile = arg
                try:
                    f = open(self.marketFile, "r")
                    for line in f:
                        infos = line.split()
                        if infos[0][0] != '#':
                            self.markets[infos[0]] = Market(infos[0], infos[1], infos[2])
                except IOError as e:
                    self.ExitUsage(1, "Bad arguments. Failed to open the markets description file.")
            elif opt == "--testmode":
                Globales.testMode = 1
                Globales.testModeFile = arg
        if marketFileDefined == 0:
            self.ExitUsage(1, "Bad arguments. Please define a markets description file.")

    # recursive method to catch ctrl-c
    def Join(self, threads):
        try:
            for t in threads:
                t.join()
        # manage interupt ctrl-c, to quit the bot properly
        # cleanup and quit
        except (KeyboardInterrupt, SystemExit):
            print("Terminating bot.")
            Globales.stopBot = 1
            self.Join(threads)

    # launch market threads
    def Run(self):
        threads = []
        for m in self.markets.items():
            t = threading.Thread(target=m[1].Run, args=[])
            t.start()
            threads.append(t)
        self.Join(threads)

trader = BTCTrader(sys.argv[1:])
trader.Run()
