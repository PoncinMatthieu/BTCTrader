
import time
from hashlib import sha512
from hmac import HMAC
import base64
from urllib import urlencode

from Requester import Requester

def get_nonce():
    return int(time.time()*100000)

def sign_data(secret, data):
    return base64.b64encode(str(HMAC(secret, data, sha512).digest()))


class MtGoxRequester(Requester):
    def __init__(self, authId, authPass):
        Requester.__init__(self, "https://mtgox.com/api/1/")
        self.authKey = authId
        self.authSecret = base64.b64decode(authPass)

    def BuildQuery(self, req={}):
        req["nonce"] = get_nonce()
        postData = urlencode(req)
        headers = {}
        headers["User-Agent"] = "GoxApi"
        headers["Rest-Key"] = self.authKey
        headers["Rest-Sign"] = sign_data(self.authSecret, postData)
        return (postData, headers)
