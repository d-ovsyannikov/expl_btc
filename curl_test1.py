import requests
import json

url = 'http://user1203:Dr3Ld0z[sqfR4@127.0.0.1:8332/'
# headers = {'Content-type': 'application/json',}
data1 = '{"jsonrpc": "1.0", "id":"curltest", "method": "getblockhash", "params": [728000] }'
data2 = '{"jsonrpc": "1.0", "id": "curltest", "method": "getblock", "params": ["00000000000000000001b090122f97d34fe53fe26df734d7c0f6b6d527add5ca", 2]}'
r = requests.post(url,  data=data2)
print (r)
print (r.json())