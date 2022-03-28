import bitcoin.rpc as rpc

proxy = rpc.Proxy()
proxy.getinfo()
# print(proxy.getnewaddress())