import urllib.request as urllib
import xml.etree.ElementTree as ET

class Api:
    def requestApi(self,endpoint,xmldata):
        entrypoint = "https://api.unas.eu/shop/"
 
        request = urllib.Request(entrypoint + endpoint, data=xmldata)

        request.add_header("Content-Type", "application/xml")

        response = urllib.urlopen(request)

        print(response.read())

        root = ET.fromstring(response)
        return root

    def AuthByKey(self,apikey):
        return Api.requestApi(self,"login","""<?xml version="1.0" encoding="UTF-8" ?>
			<Params>
				<ApiKey>{apikey_temp}</ApiKey>
			</Params>""".format(apikey_temp=apikey) )