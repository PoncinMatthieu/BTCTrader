
import urllib2
import json

class Requester:
    def __init__(self, basePath):
        self.basePath = basePath

    def BuildQuery(self, req={}):
        print("Method not implemented !")

    def Perform(self, path, args):
        data, headers = self.BuildQuery(args)
        req = urllib2.Request(self.basePath + path, data, headers)
        res = urllib2.urlopen(req, data)
        return json.load(res)

