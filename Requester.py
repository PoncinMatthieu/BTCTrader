
import json
import urllib

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
        if data != None:
            data = data.encode('ascii')
        req = urllib.request.Request(self._apiUri + url, data, headers)
        res = urllib.request.urlopen(req)
        encoding = res.headers.get_content_charset()
        body = res.read().decode(encoding)
        jsonResponse = json.loads(body)
        if Globales.verbose == 1:
            print("Response:")
            print(jsonResponse)
        return jsonResponse

    def BuildQuery(self, req={}):
        print("Method to redefine !")

    def GetAccount(self):
        print("Method to redefine !")

