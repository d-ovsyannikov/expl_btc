import requests
import json

rpcUrl = 'http://username:password@127.0.0.1:8332/'
# headers = {'Content-type': 'application/json',}
data1 = '{"jsonrpc": "1.0", "id":"curltest", "method": "getblockhash", "params": [728000] }'
data2 = '{"jsonrpc": "1.0", "id": "curltest", "method": "getblock", "params": ["00000000000000000001b090122f97d34fe53fe26df734d7c0f6b6d527add5ca", 2]}'
data3 = '{"jsonrpc": "1.0", "id":"curltest", "method": "getrawtransaction", "params": ["db102946b5971045e213a6f0718f779d7d9bb533f7a4ce66d77c030afa77fc97", true] }'
r = requests.post(rpcUrl,  data=data3)
print (r)
print (r.json())