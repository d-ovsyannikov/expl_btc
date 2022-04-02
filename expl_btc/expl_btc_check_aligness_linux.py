import requests
import mysql.connector as mysql
import json
import numpy as np
import time
import sys

rpcUrl = 'http://username:password@127.0.0.1:8332/'
# rpcUrl = 'http://user1203:Dr3Ld0z[sqfR4@localhost:8332/'

#-----------------------------------------------------------------------------------------------
def getMinMaxBlockInDB():
	return (10, 20)
#-----------------------------------------------------------------------------------------------
def getBlockchainHeight():
	query = '{"jsonrpc": "1.0", "id":"curltest", "method": "getblockchaininfo" }'
	r = requests.post(rpcUrl,  data=query)
	if not r.ok:
		print ("BTC-Core RPC getblockhash call error:", r)
		exit()
	return int(r.json()["result"]["blocks"])
#-----------------------------------------------------------------------------------------------
def printProgressBar(iteration, total, decimals=1, length=50):
	str_format = "{0:." + str(decimals) + "f}"
	percents = str_format.format(100 * (iteration / float(total)))
	abs_values = "(%d/%d)" %(iteration, total)
	filled_length = int(round(length * iteration / float(total)))
	bar = '█' * filled_length + '-' * (length - filled_length)

	sys.stdout.write('\r%s |%s| %s%s %s' % ("Blocks read:", bar, percents, '%', abs_values))

	if iteration == total:
		sys.stdout.write('\n')
	sys.stdout.flush()
#-----------------------------------------------------------------------------------------------

print ("###### BTC-blockchain synchronization utility ######")

# Connect to DB
db = mysql.connect(
    host = "localhost",
    user = "expl_btc",
	# user = "root",
    passwd = "Gfhjkmgfhjkm1",
    database = "expl_btc_db"
	# database = "datacamp"
)
cursor = db.cursor()
print ("DB connection [OK]")

# Check if tables exists, if not - create
query = "SHOW TABLES LIKE 'outs';"
cursor.execute(query)
r = cursor.fetchall()
query = "SHOW TABLES LIKE 'ins';"
cursor.execute(query)
r2 = cursor.fetchall()

if len(r) == 0:	
	print ("DB: 'outs' table not found, all data dropped, tables recreated")
	if len(r2) != 0:
		cursor.execute("DROP TABLE ins;")

if len(r2) == 0:
	if len(r) != 0:
		print ("DB: 'ins' table not found, all data dropped, tables recreated")
		cursor.execute("DROP TABLE outs;")
	
if len(r2) == 0 or len(r) == 0:
	cursor.execute("CREATE TABLE outs (id BIGINT NOT NULL PRIMARY KEY auto_increment, txid VARCHAR(255), addr VARCHAR(255), out_ind INT, value FLOAT, block INT)")
	cursor.execute("CREATE TABLE ins (id BIGINT NOT NULL PRIMARY KEY auto_increment, txid VARCHAR(255), out_ind INT, block INT)")
	# cursor.execute("ALTER TABLE `outs` ADD INDEX `addr_index` (`addr`);")
	# cursor.execute("ALTER TABLE `ins` ADD INDEX `txid_index` (`txid`);")

print ("Bitcoin-core RPC connection [OK]")

cursor.execute("SELECT MAX(block) FROM outs;")
r = cursor.fetchall()
cursor.execute("SELECT MIN(block) FROM outs;")
r2 = cursor.fetchall()

# print(r[0][0], r2)

if r2[0][0] == None or r[0][0] == None:
	print ("Blockchain height: %d, loaded to DB 0, 0%%" %(getBlockchainHeight()))
else:
	minBlockInDB = int(r2[0][0])
	maxBlockInDB = int(r[0][0])
	print ("Blockchain height: %d, loaded to DB %d (from %d to %d), %f%%" %(getBlockchainHeight(), maxBlockInDB - minBlockInDB + 1, minBlockInDB, maxBlockInDB, (maxBlockInDB - minBlockInDB + 1)/getBlockchainHeight()))
	print ("Trim boundary blocks [OK]")

# print ("Loading newest blocks:")
# print ("Loading historical blocks")

startBlock = 729580
finalBlock = 600000
# startBlock = 727579
# finalBlock = 729280

overall_start = time.time()
for blockNum in range(startBlock, finalBlock, -1):	
	# start = time.time()
	# Get block hash
	query = '{"jsonrpc": "1.0", "id":"curltest", "method": "getblockhash", "params": [%d] }' %blockNum
	r = requests.post(rpcUrl,  data=query)
	if not r.ok:
		print ("BTC-Core RPC getblockhash call error:", r)
		exit()
	blockHash = (r.json())["result"]

	# Get raw block data
	query = '{"jsonrpc": "1.0", "id": "curltest", "method": "getblock", "params": ["%s", 2]}' %blockHash
	r = requests.post(rpcUrl,  data=query)
	if not r.ok:
		print ("BTC-Core RPC getblock call error:", r)
		exit()
	block = (r.json())["result"]

	# print ("Block", blockNum, "read, number of TXs", len(block["tx"]))

	# Add new txs to DB
	for tx in block["tx"]:
		# query = "INSERT INTO txs (txid) VALUES ('%s')" %(tx["txid"])
		# cursor.execute(query)
		# cursor.execute("SELECT LAST_INSERT_ID();")
		# txTableId = (cursor.fetchall())[0][0]
		ind = 0
		for out in tx["vout"]:
			if "addresses" in out["scriptPubKey"]:
				query = "INSERT INTO outs (txid, addr, out_ind, value, block) VALUES ('%s', %s, %d, %f, %d)" %(tx["txid"], json.dumps(out["scriptPubKey"]["addresses"][0]), ind, out["value"], blockNum)
				cursor.execute(query)
			if "address" in out["scriptPubKey"]:
				query = "INSERT INTO outs (txid, addr, out_ind, value, block) VALUES ('%s', %s, %d, %f, %d)" %(tx["txid"], json.dumps(out["scriptPubKey"]["address"]), ind, out["value"], blockNum)
				cursor.execute(query)

			ind = ind + 1

		for ins in tx["vin"]:
			if "txid" in ins:
				query = "INSERT INTO ins (txid, out_ind, block) VALUES (%s, %d, %d)" %(json.dumps(ins["txid"]), ins["vout"], blockNum)
				cursor.execute(query)
	db.commit()
	printProgressBar(-blockNum+startBlock, -finalBlock+startBlock)
printProgressBar(-finalBlock+startBlock, -finalBlock+startBlock)
print()
				
	# end = time.time()
	# print (np.around((end - start) , decimals=2), "sec. for block")

overall_end = time.time()
print (np.around((overall_end - overall_start) , decimals=2), "sec. in total")