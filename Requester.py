
import urllib2
import json

import Globales

class Requester:
    def __init__(self, apiUri):
        self._apiUri = apiUri

    def Perform(self, url, args):
        global _verbose
        data, headers = self.BuildQuery(args)
        if Globales.verbose == 1:
            print("Sending request:")
            print(self._apiUri + url)
            print(data)
            print(headers)
        req = urllib2.Request(self._apiUri + url, data, headers)
        res = urllib2.urlopen(req)
        jsonResponse = json.load(res)
        if Globales.verbose == 1:
            print("Response:")
            print(jsonResponse)
        return jsonResponse

    def BuildQuery(self, req={}):
        print("Method to redefine !")

    def GetAccount(self):
        print("Method to redefine !")

