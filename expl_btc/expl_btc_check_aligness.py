import requests
import mysql.connector as mysql

rpcUrl = 'http://username:password@127.0.0.1:8332/'

# Obtain hash of block N1
blockNum = 1
query = '{"jsonrpc": "1.0", "id":"curltest", "method": "getblockhash", "params": [%d] }' %blockNum
r = requests.post(rpcUrl,  data=query)
if not r.ok:
	print ("BTC-Core RPC call error:", r)
blockHash = (r.json())["result"]

# Get raw block data
query = '{"jsonrpc": "1.0", "id": "curltest", "method": "getblock", "params": ["%s", 2]}' %blockHash
r = requests.post(rpcUrl,  data=query)
if not r.ok:
	print ("BTC-Core RPC call error:", r)
block = (r.json())["result"]


# Connect to DB
db = mysql.connect(
    host = "localhost",
    user = "expl_btc",
    passwd = "Gfhjkmgfhjkm3",
    database = "expl_btc_db"
)
cursor = db.cursor()

# Check if tables exists, if not - create
query = "SHOW TABLES LIKE 'txs';"
cursor.execute(query)
r = cursor.fetchall()
if len(r) != 0:
	cursor.execute("SELECT COUNT(*) FROM txs;")
	r = cursor.fetchall()
	print ("TXs table exists, rows: ",r[0][0])
	cursor.execute("DROP TABLE txs;")
cursor.execute("CREATE TABLE txs (id BIGINT NOT NULL PRIMARY KEY auto_increment, txid VARCHAR(255))")

# Add new txs to DB
for tx in block["tx"]:
	query = "INSERT INTO txs (txid) VALUES ('%s')" %(tx["txid"])
	cursor.execute(query)

cursor.execute("SELECT COUNT(*) FROM txs;")
r = cursor.fetchall()
print ("TXs table exists, rows: ",r[0][0])