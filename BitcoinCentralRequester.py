import base64
import json
import urllib.request
import urllib.parse

from Account import Account
from Requester import Requester



#the method to authenticate will change soon
#btc-central plans to move to OAuthv2 from basic http auth
class BitcoinCentralRequester(Requester):
    def __init__(self, authId, authPass):
        Requester.__init__(self, 'https://bitcoin-central.net/api/v1/')
        self.authId = authId
        self.authPass = authPass
        concat = authId + ':' + authPass
        self.authHttpBase64 = base64.b64encode(concat.encode())

    def BuildQuery(self, reqs={}):
        headers = {}
        postData = urllib.parse.urlencode(reqs)
        headers["Content-Type"] = 'application/json'
        headers["Authorization"] = 'Basic ' + self.authHttpBase64.decode('ascii')
        return (postData, headers)

        
    def GetAccount(self):
        #actually, there is no way yet to get informations from
        #the bitcoin-central API but it would be a call to "/me"
        #check the https://bitcoin-central.net/s/api-v1-documentation
        #it should change soon
        #now I only get the current balance
        res = self.Perform("account_operations", {})
        print(res)
        a = Account()
        return a
