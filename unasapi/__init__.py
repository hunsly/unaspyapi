
import requests

import xml.etree.ElementTree as ET

class Api:
    __token = ''

    def requestApi(self,endpoint,xmldata):

        entrypoint = "https://api.unas.eu/shop/"
 
        url = entrypoint + endpoint
        headers = {}
        headers['Content-Type'] = "application/xml"

        r = requests.post(url, headers=headers, data=xmldata)

        root = ET.fromstring(r.content)
        return root

    def AuthByKey(self,apikey):
        req = Api.requestApi(self,"login","""<?xml version="1.0" encoding="UTF-8" ?>
			<Params>
				<ApiKey>{apikey_temp}</ApiKey>
			</Params>""".format(apikey_temp=apikey) )
        
        if (req.tag == 'Error'):
             raise AuthByKeyError(req.text)
        return 

class AuthByKeyError(Exception):
    def __init__(self, message):
        self.message = 'Unas api error' + message
        super().__init__(self.message)