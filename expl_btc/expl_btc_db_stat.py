import mysql.connector as mysql

db = mysql.connect(
    host = "localhost",
    user = "expl_btc",
    passwd = "Gfhjkmgfhjkm3",
    database = "datacamp"
)

# print(db) # it will print a connection object if everything is fine
cursor = db.cursor()
cursor.execute("SHOW TABLES LIKE 'txs'")