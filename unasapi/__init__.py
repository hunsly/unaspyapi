
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
        root = ET.Element("Params")
        ET.SubElement(root, "ApiKey").text = apikey

        req = Api.callApi(self, "login", ET.tostring(root, xml_declaration=True, encoding='utf-8'))

        if (req.tag == 'Error'):
            raise AuthByKeyError(req.text)

        if (req.find("Status").text != 'ok'):
            raise AuthByKeyError("Status is not OK ")

        self.__tokenExpire = datetime.strptime(
            req.find("Expire").text, "%Y.%m.%d %H:%M:%S")
        self.__token = req.find("Token").text


    ORDER_STATUS_OPEN_NORMAL = "open_normal"    # normál nyitott rendelés
    ORDER_STATUS_CLOSE_OK = "close_ok"          # sikeresen lezárt rendelés
    ORDER_STATUS_CLOSE_FAULT = "close_fault"    # sikertelenül lezárt rendelés
    ORDER_STATUSES = [
        ORDER_STATUS_OPEN_NORMAL,
        ORDER_STATUS_CLOSE_OK ,
        ORDER_STATUS_CLOSE_FAULT
    ]

    ORDER_INVOICE_STATUS_NOT_BILLABLE = 0   # nem számlázható
    ORDER_INVOICE_STATUS_BILLABLE = 1       # számlázható
    ORDER_INVOICE_STATUS_BILLED = 2         # számlázva
    ORDER_INVOICE_STATUSES = [
        ORDER_INVOICE_STATUS_NOT_BILLABLE,
        ORDER_INVOICE_STATUS_BILLABLE,
        ORDER_INVOICE_STATUS_BILLED
    ]

    # Az alábbi végpont visszaadja a kérésében meghatározott feltételeknek megfelelő rendelés vagy rendelések adatait
    def getOrder(self,**kwargs):
        root = ET.Element("Params")

        # rendelés aktuális státuszának típusa, vagy sorszáma
        if 'Status' in kwargs and (
                kwargs['Status'] in ORDER_STATUSES
                or is_integer(kwargs['Status'])):
            ET.SubElement(root, "Status").text = kwargs['Status']
        
        # rendelés aktuális státuszának egyedi azonosítója
        if 'StatusKey' in kwargs:
            ET.SubElement(root, "StatusKey").text = kwargs['StatusKey']
        
        # rendelés aktuális státuszának egyedi azonosítója
        if 'Email' in kwargs:
            ET.SubElement(root, "Email").text = kwargs['Email']
            
        # rendelés számlázási státusza
        if 'InvoiceStatus' in kwargs and kwargs['InvoiceStatus'] in ORDER_INVOICE_STATUSES:
            ET.SubElement(root, "InvoiceStatus").text = kwargs['InvoiceStatus']
        
        # rendelésen be van állítva az automatikus számlázási státusz állítás
        if 'InvoiceAutoSet' in kwargs and kwargs['InvoiceAutoSet'] == True:
            ET.SubElement(root, "InvoiceAutoSet").text = 1

        # unix timestamp, ezen időpont utáni rendelések listázása
        if 'TimeStart' in kwargs and isinstance(kwargs['TimeStart'], datetime.date):
            ET.SubElement(root, "TimeStart").text = kwargs['TimeStart'].strftime("%s")

        # unix timestamp, ezen időpont előtti rendelések listázása
        if 'TimeEnd' in kwargs and isinstance(kwargs['TimeEnd'], datetime.date):
            ET.SubElement(root, "TimeEnd").text = kwargs['TimeEnd'].strftime("%s")

        # dátum utáni rendelések listázása 
        if 'DateStart' in kwargs and isinstance(kwargs['DateStart'], datetime.date):
            ET.SubElement(root, "DateStart").text = kwargs['DateStart'].strftime("%Y.%m.%d")

        # dátum előtti rendelések listázása 
        if 'DateEnd' in kwargs and isinstance(kwargs['DateEnd'], datetime.date):
            ET.SubElement(root, "DateEnd").text = kwargs['DateEnd'].strftime("%Y.%m.%d")

        # unix timestamp, ezen időpont utáni módosult rendelések listázása
        if 'TimeModStart' in kwargs and isinstance(kwargs['TimeModStart'], datetime.date):
            ET.SubElement(root, "TimeModStart").text = kwargs['TimeModStart'].strftime("%s")

        # unix timestamp, ezen időpont előtti módosult rendelések listázása
        if 'TimeModEnd' in kwargs and isinstance(kwargs['TimeModEnd'], datetime.date):
            ET.SubElement(root, "TimeModEnd").text = kwargs['TimeModEnd'].strftime("%s")
        
        # hányadik rendeléstől induljon a letöltés, pozitív egész szám, csak a LimitNum paraméterrel együtt használható
        if ('LimitStart' in kwargs 
                and type(kwargs['LimitStart']) is int
                and kwargs['LimitStart'] > 0
                and 'LimitNum' in kwargs):
            ET.SubElement(root, "LimitStart").text = kwargs['LimitStart']
        elif ('LimitNum' in kwargs
                and type(kwargs['LimitNum']) is int
                and kwargs['LimitNum'] > 0
                and kwargs['LimitNum'] <= 500):
            ET.SubElement(root, "LimitNum").text = kwargs['LimitNum']
        
        # egyedi rendelés azonosító, csak egy konkrét rendelés adatainak lekéréséhez
        if 'Key' in kwargs:
            ET.SubElement(root, "Key").text = kwargs['Key']

        if len(list(root)) == 0:
            raise GetOrderEmptyRequestError("Request is epmty!")
        
        req = Api.callApi(self, "getOrder", ET.tostring(root, xml_declaration=True, encoding='utf-8'))

        if (req.tag == 'Error'):
            raise GetOrderResponseError(req.text)

        return req
        

class AuthByKeyError(Exception):
    def __init__(self, message):
        self.message = 'Unas api error: ' + message
        super().__init__(self.message)

class GetOrderEmptyRequestError(Exception):
    def __init__(self, message):
        self.message = 'Unas api error: ' + message
        super().__init__(self.message)


class GetOrderResponseError(Exception):
    def __init__(self, message):
        self.message = 'Unas api error: ' + message
        super().__init__(self.message)
