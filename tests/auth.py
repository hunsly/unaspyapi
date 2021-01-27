

import unasapi

unasTestApi = unasapi.Api()

try:
    unasTestApi.AuthByKey('dfsdfsd')
except unasapi.AuthByKeyError:
    print("AuthByKeyError: OK")


try:
    unasTestApi.AuthByKey('XXXXXXXXXXXX')
    print("AuthByKey: OK")
except:
    print("AuthByKey: FAIL ")
    raise