
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
    raise