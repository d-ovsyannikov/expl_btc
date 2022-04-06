from xml.etree.ElementTree import tostring
import requests
import mysql.connector as mysql
import json
import numpy as np
import time
import sys
from queue import SimpleQueue

class Fifo(SimpleQueue):
    def __iter__(self):
        return self

    def __len__(self):
        return self.qsize()

    def __next__(self):
        if not self.empty():
            return self.get()
        raise StopIteration

rpcUrl = 'http://username:password@127.0.0.1:8332/'
# rpcUrl = 'http://user1203:Dr3Ld0z[sqfR4@localhost:8332/'

#-----------------------------------------------------------------------------------------------
def getMinMaxBlockInDB():
	cursor.execute("SELECT MAX(block) FROM outs;")
	r = cursor.fetchall()
	cursor.execute("SELECT MIN(block) FROM outs;")
	r2 = cursor.fetchall()
	# print (r,r2)
	return [r2[0][0], r[0][0]]
#-----------------------------------------------------------------------------------------------
def getBlockchainHeight():
	query = '{"jsonrpc": "1.0", "id":"curltest", "method": "getblockchaininfo" }'
	r = requests.post(rpcUrl,  data=query)
	if not r.ok:
		print ("BTC-Core RPC getblockhash call error:", r)
		exit()
	return int(r.json()["result"]["blocks"])
#-----------------------------------------------------------------------------------------------
def printProgressBar(iteration, total, estTime, decimals=1, length=50):
	str_format = "{0:." + str(decimals) + "f}"
	percents = str_format.format(100 * (iteration / float(total)))
	abs_values = "(%d/%d)" %(iteration, total)
	filled_length = int(round(length * iteration / float(total)))
	bar = '█' * filled_length + '-' * (length - filled_length)
	# ETC = ""
	estTime = estTime / 60
	days = estTime //  1440
	hours = (estTime - days*1440) // 60
	mins = estTime - days*1440 - hours*60
	if days != 0:
			ETC = "%d days, %d hours, %d min" %(days,hours, mins)

	else:
		if hours != 0:
			ETC = "%d hours, %d min" %(hours, mins)
		else:
			ETC = "%d min" %(mins)

	sys.stdout.write('\r%s |%s| %s%s %s ETC: %s' % ("Blocks read:", bar, percents, '%', abs_values, ETC))

	if iteration == total:
		sys.stdout.write('\n')
	sys.stdout.flush()
#-----------------------------------------------------------------------------------------------
def addBlock(blockNum):
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
				query = "INSERT INTO ins (tx_src, tx_dst, out_ind, block) VALUES ('%s', '%s', %d, %d)" %(ins["txid"], tx["txid"], ins["vout"], blockNum)
				cursor.execute(query)	
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
	cursor.execute("CREATE TABLE ins (id BIGINT NOT NULL PRIMARY KEY auto_increment, tx_src VARCHAR(255),tx_dst VARCHAR(255), out_ind INT, block INT)")
	# cursor.execute("ALTER TABLE `outs` ADD INDEX `addr_index` (`addr`);")
	# ALTER TABLE `outs` ADD INDEX `block_index` (`block`), ADD INDEX `addr_index` (`addr`);
	# cursor.execute("ALTER TABLE `ins` ADD INDEX `tx_src_index` (`tx_src`);")
	# ALTER TABLE `ins` ADD INDEX `block_index` (`block`), ADD INDEX `tx_src_index` (`tx_src`), ADD INDEX out_ind_index (out_ind);

print ("Bitcoin-core RPC connection [OK]")

minMaxBlockInDB = getMinMaxBlockInDB()

# print(r[0][0], r2)
highestBlock = getBlockchainHeight()

if minMaxBlockInDB[0] == None or minMaxBlockInDB[1] == None:
	print ("Blockchain height: %d, loaded to DB 0, 0%%" %(highestBlock))
else:
	print ("Blockchain height: %d, loaded to DB %d (from %d to %d), %f%%" %(highestBlock, minMaxBlockInDB[1] - minMaxBlockInDB[0] + 1, minMaxBlockInDB[0], minMaxBlockInDB[1], (minMaxBlockInDB[1] - minMaxBlockInDB[0] + 1)*100.0/highestBlock))
	cursor.execute("DELETE FROM outs WHERE block=%d;" %minMaxBlockInDB[0])
	cursor.execute("DELETE FROM outs WHERE block=%d;" %minMaxBlockInDB[1])
	cursor.execute("DELETE FROM ins WHERE block=%d;" %minMaxBlockInDB[0])
	cursor.execute("DELETE FROM ins WHERE block=%d;" %minMaxBlockInDB[1])
	print ("Trim boundary blocks [OK]")
	if minMaxBlockInDB[0] == minMaxBlockInDB[1]:
		minMaxBlockInDB = (None, None)
	else:
		minMaxBlockInDB[1] = minMaxBlockInDB[1] - 1
		minMaxBlockInDB[0] = minMaxBlockInDB[0] + 1
	

commitCounter = 0
commitEveryNBlocks = 10
# start = time.time()
# estBlockTime = 0

# timeQueue = Fifo()
timeQueue = []
maxTimeQueueLen = 150
avgTime = 0

# print (np.around((end - start) , decimals=2), "sec. for block")
if minMaxBlockInDB[0]:
	if minMaxBlockInDB[1] < highestBlock:
		print ("Loading newest blocks:")
		
		cursor.execute("ALTER TABLE outs DISABLE KEYS;")
		cursor.execute("ALTER TABLE ins DISABLE KEYS;")
		cursor.execute("SET autocommit=0;")
		
		for blockNum in range(minMaxBlockInDB[1], highestBlock, 1):
			start = time.time()
			addBlock(blockNum)
			end = time.time()
			timeQueue.append(end-start)
			if (len(timeQueue) >= maxTimeQueueLen):
				timeQueue.pop(0)
			avgTime = 0
			for i3 in timeQueue:
				avgTime = avgTime + i3
			avgTime = avgTime/len(timeQueue)
			start = end

			printProgressBar(blockNum-minMaxBlockInDB[1], highestBlock-minMaxBlockInDB[1] + 1, (highestBlock - blockNum)* avgTime)
			commitCounter = commitCounter + 1
			if commitCounter >= commitEveryNBlocks:
				commitCounter = 0
				db.commit()
				# end = time.time()
				# estBlockTime = (end - start)/commitEveryNBlocks
				# start = time.time()

		printProgressBar(highestBlock-minMaxBlockInDB[1] + 1, highestBlock-minMaxBlockInDB[1] + 1, 0)
		cursor.execute("SET autocommit=1;")


if (minMaxBlockInDB[0] != 0):
	print ("Loading historical blocks:")
	if minMaxBlockInDB[0] == None:
		startBlock = highestBlock
	else:
		startBlock = minMaxBlockInDB[0] - 1

	finalBlock = 0

	cursor.execute("ALTER TABLE outs DISABLE KEYS;")
	cursor.execute("ALTER TABLE ins DISABLE KEYS;")
	cursor.execute("SET autocommit=0;")
			
	for blockNum in range(startBlock, finalBlock, -1):
		start = time.time()
		addBlock(blockNum)
		end = time.time()
		timeQueue.append(end-start)
		if (len(timeQueue) >= maxTimeQueueLen):
			timeQueue.pop(0)
		avgTime = 0
		for i3 in timeQueue:
			avgTime = avgTime + i3
		avgTime = avgTime/len(timeQueue)
		start = end


		printProgressBar(-blockNum+startBlock, -finalBlock+startBlock, blockNum* avgTime)
		# printProgressBar(blockNum-minMaxBlockInDB[1], highestBlock-minMaxBlockInDB[1] + 1, (highestBlock - blockNum)* estBlockTime)
		commitCounter = commitCounter + 1
		if commitCounter >= commitEveryNBlocks:
			commitCounter = 0
			db.commit()
			# print ((end - start)/commitEveryNBlocks)
			# estBlockTime = (end - start)/commitEveryNBlocks
			# start = time.time()

	# printProgressBar(highestBlock-minMaxBlockInDB[1] + 1, highestBlock-minMaxBlockInDB[1] + 1)
	printProgressBar(-finalBlock+startBlock, -finalBlock+startBlock, 0)
	cursor.execute("SET autocommit=1;")

# startBlock = 729580
# finalBlock = 600000
# startBlock = 727579
# finalBlock = 729280

exit()

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
				query = "INSERT INTO ins (tx_src, tx_dst, out_ind, block) VALUES ('%s', '%s', %d, %d)" %(ins["txid"], tx["txid"], ins["vout"], blockNum)
				cursor.execute(query)
	db.commit()
	printProgressBar(-blockNum+startBlock, -finalBlock+startBlock)
printProgressBar(-finalBlock+startBlock, -finalBlock+startBlock)
print()
				
	# end = time.time()
	# print (np.around((end - start) , decimals=2), "sec. for block")

overall_end = time.time()
print (np.around((overall_end - overall_start) , decimals=2), "sec. in total")