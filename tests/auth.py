
import json
import unasapi

with open( "tests/config.json", 'r') as file:
    data_JSON = json.load(file)

unasTestApi = unasapi.Api()

try:
    unasTestApi.AuthByKey('dfsdfsd')
except unasapi.AuthByKeyError:
    print("AuthByKeyError: OK")


try:
    unasTestApi.AuthByKey(data_JSON['apikey'])
    print("AuthByKey: OK")
except:
    print("AuthByKey: FAIL")

try:
    unasTestApi.getOrder()
    print("getOrder empty args: FAIL")
except unasapi.GetOrderEmptyRequestError:
    print("AuthByKey empty args: OK")

try:
    unasTestApi.getOrder(Key="82082-526197")
    print("getOrder good key: OK")
except unasapi.GetOrderEmptyRequestError:
    print("AuthByKey good key: FAIL")
    

