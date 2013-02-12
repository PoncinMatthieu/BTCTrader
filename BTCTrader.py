#!/usr/bin/python

import sys
import getopt

import Globales
from Requester import Requester
from MtGoxRequester import MtGoxRequester


class BTCTrader:
    def ExitUsage(self, error=0, msg=""):
        if error != 0:
            print("Error: " + msg)
        print("usage: ./BTCTrader.py [OPTION] --api=[mtgox|bitcoin-central] --authId=[ID] --authPass=[PASS]")
        print("OPTION:")
        print("\t-h, --help: print usage")
        print("\t-v, --verbose: verbose mode")
        sys.exit(error)

    # constructor, here we take care of the arguments.
    # print the usage if something is wrong
    def __init__(self, argv):
        self.api = ""
        self.authId = ""
        self.authPass = ""
        try:
            opts, args = getopt.getopt(argv, "hv", ["help", "verbose", "api=", "authId=", "authPass="])
        except getopt.GetoptError:
            self.ExitUsage(1, "Bad arguments.")
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                self.ExitUsage()
            elif opt in ("-v", "--verbose"):
                Globales.verbose = 1
            elif opt == "--api":
                self.api = arg
            elif opt == "--authId":
                self.authId = arg
            elif opt == "--authPass":
                self.authPass = arg
        if self.api not in ("mtgox", "bitcoin-central") or len(self.authId) == 0 or len(self.authPass) == 0:
            self.ExitUsage(1, "Bad arguments.")

    def CreateRequester(self):
        if (self.api == "mtgox"):
            return MtGoxRequester(self.authId, self.authPass)
        elif (self.api == "bitcoin-central"):
            print("please implement me :'(")
            sys.exit()

    def Run(self):
        try:
            req = self.CreateRequester()
            account = req.GetAccount()
            print(account)
        except:
            print("Unexpected error: ")
            print(sys.exc_info())


trader = BTCTrader(sys.argv[1:])
trader.Run()
