import requests
import json

# Get hash of block 728000
# Get full block
# 
url = 'http://user1203:Dr3Ld0z[sqfR4@localhost:8332/'
# headers = {'Content-type': 'application/json',}
query1 = '{"jsonrpc": "1.0", "id":"curltest", "method": "getblockhash", "params": [728700] }'
r = requests.post(url,  data=query1)
if not r.ok:
	print ("Error: Unable to obtain block hash by RPC")
	exit()

r = r.json()
blockHash = r["result"]

query2 = '{"jsonrpc": "1.0", "id": "curltest", "method": "getblock", "params": ["%s", 2]}' %blockHash
# print (query2)
r = requests.post(url,  data=query2)
if not r.ok:
	print ("Error")
	exit()
	
r = r.json()
# print (r["result"]["tx"][0])
# print (len(r["result"]["tx"][43]["vout"]))
# print (r["result"]["tx"][43]["vout"][1]["value"])
print (r["result"]["tx"][0]["vin"][0])
# a = {}
# l = []

# a["addr"] = r["result"]["tx"][43]["vout"][0]["scriptPubKey"]["addresses"]
# a["value"] = r["result"]["tx"][43]["vout"][0]["value"]
# l.append(a)
# a["addr"] = r["result"]["tx"][43]["vout"][1]["scriptPubKey"]["addresses"]
# a["value"] = r["result"]["tx"][43]["vout"][1]["value"]
# l.append(a)

# list (dict("abc", out["value"]) for out in r["result"]["tx"][43]["vout"])
# print (l)

#-----DP PART------
import mysql.connector as mysql

## connecting to the database using 'connect()' method
## it takes 3 required parameters 'host', 'user', 'passwd'
db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "Gfhjkmgfhjkm3",
    database = "datacamp"
)

print(db) # it will print a connection object if everything is fine
cursor = db.cursor()
cursor.execute("DROP TABLE txs")
# cursor.execute("CREATE TABLE txs (id BIGINT NOT NULL PRIMARY KEY auto_increment, txid VARCHAR(255), outs JSON)")
cursor.execute("CREATE TABLE txs (id BIGINT NOT NULL PRIMARY KEY auto_increment, txid VARCHAR(255))")
cursor.execute("DROP TABLE outs")
cursor.execute("CREATE TABLE outs (id BIGINT NOT NULL PRIMARY KEY auto_increment, addr VARCHAR(255), value FLOAT, txin BIGINT NOT NULL REFERENCES txs(ID), in_ind INT NOT NULL, txout BIGINT REFERENCES txs(ID), out_ind INT)")


for tx in r["result"]["tx"]:
	# print (tx["vout"][0])
	# outs_list = []
	query = "INSERT INTO txs (txid) VALUES ('%s')" %(tx["txid"])
	cursor.execute(query)
	# db.commit()
	cursor.execute("SELECT LAST_INSERT_ID();")
	txTableId = (cursor.fetchall())[0][0]

	ind = 0
	for out in tx["vout"]:
		# a = {}
		# print (out)
		# txTableId = 10
		if "addresses" in out["scriptPubKey"]:
			# a["addr"] = out["scriptPubKey"]["addresses"]
			# a["value"] = out["value"]
			# outs_list.append(a)
			query = "INSERT INTO outs (addr, value, txin, in_ind) VALUES (%s, %f, %d, %d)" %(json.dumps(out["scriptPubKey"]["addresses"][0]), out["value"], txTableId, ind)
			cursor.execute(query)
		ind = ind + 1

	# for ins in tx["vin"]:

	# query = "INSERT INTO txs (txid, outs) VALUES ('%s', '%s')" %(tx["txid"], json.dumps(outs_list)) # 
	# print (query)
	# cursor.execute(query)

## to make final output we have to run the 'commit()' method of the database object
db.commit()

# query = "SELECT values FROM txs, JSON_TABLE(outs, '$[*]' COLUMNS (value_a FLOAT  PATH '$.value')) values;"
# query = "SELECT CAST(outs -> '$[*].value' AS UNSIGNED ARRAY) FROM txs WHERE outs -> '$[*].value' > 1;"
# query = "SELECT * FROM JSON_TABLE('%s','$[*]' COLUMNS( c1 INT PATH '$.c1' ERROR ON ERROR )) as jt;" %('[ {"c1": null} ]')
## getting records from the table
# query = "SELECT id FROM outs WHERE txin = 'bf0d0ee9092036ab12f81e8b174a7f0fe8734f77eefab15c5535b6230d7cd2c8' AND in_ind = 0;"
query = "SELECT COUNT(*) FROM txs;"

# cursor.execute("DROP TABLE txs")
# query = "SHOW TABLES LIKE 'txs';"
cursor.execute(query)
r = cursor.fetchall()
print (r[0][0])
# if len(r) == 0:
# 	print ("Table txs doesn't exists.")
# else:
# 	print ("Table txs exists.")


## fetching all records from the 'cursor' object
# print ((cursor.fetchall()))
# records = cursor.fetchall()

# # Showing the data
# for record in records:
#     print(record)

# query = "SELECT TABLE_NAME AS `Table`, ROUND((DATA_LENGTH + INDEX_LENGTH) / 1024 ) AS `Size (KB)` FROM information_schema.TABLES ORDER BY (DATA_LENGTH + INDEX_LENGTH) DESC"
# cursor.execute(query)
# records = cursor.fetchall()
# for record in records:
#     print(record)
