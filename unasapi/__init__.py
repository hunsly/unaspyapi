
import requests

import xml.etree.ElementTree as ET

from datetime import datetime


class Api:
    __token = ''
    __tokenExpire = ''

    def callApi(self, endpoint, xmldata):

        entrypoint = "https://api.unas.eu/shop/"

        url = entrypoint + endpoint
        headers = {}
        headers['Content-Type'] = "application/xml"

        if (self.__token != ''):
            headers['Authorization'] = "Bearer " + self.__token

        r = requests.post(url, headers=headers, data=xmldata)

        root = ET.fromstring(r.content)
        return root

    def AuthByKey(self, apikey):
        req = Api.callApi(self, "login", """<?xml version="1.0" encoding="UTF-8" ?>
			<Params>
				<ApiKey>{apikey_temp}</ApiKey>
			</Params>""".format(apikey_temp=apikey))

        if (req.tag == 'Error'):
            raise AuthByKeyError(req.text)

        if (req.find("Status").text != 'ok'):
            raise AuthByKeyError("Status is not OK ")

        self.__tokenExpire = datetime.strptime(
            req.find("Expire").text, "%Y.%m.%d %H:%M:%S")
        self.__token = req.find("Token").text


class AuthByKeyError(Exception):
    def __init__(self, message):
        self.message = 'Unas api error: ' + message
        super().__init__(self.message)
