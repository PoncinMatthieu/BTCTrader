
import urllib2
import json

import Globales

class Requester:
    def __init__(self, basePath):
        self.basePath = basePath

    def Perform(self, path, args):
        global _verbose
        data, headers = self.BuildQuery(args)
        if Globales.verbose == 1:
            print("Sending request:")
            print(self.basePath + path)
            print(data)
            print(headers)
        req = urllib2.Request(self.basePath + path, data, headers)
        res = urllib2.urlopen(req, data)
        jsonResponse = json.load(res)
        if Globales.verbose == 1:
            print("Response:")
            print(jsonResponse)
        return jsonResponse

    def BuildQuery(self, req={}):
        print("Method to redefine !")

    def GetAccount(self):
        print("Method to redefine !")

