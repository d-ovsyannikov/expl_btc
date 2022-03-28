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
cursor.execute("CREATE TABLE txs (id INT(11) NOT NULL PRIMARY KEY, name VARCHAR(255), user_name VARCHAR(255), addr JSON NOT NULL)")

query = "INSERT INTO txs (id, name, user_name, addr) VALUES (%s, %s, %s, %s)"
## storing values in a variable
values = [
    ("1", "Peter", "peter", '{"screen": "50 inch", "resolution": "2048 x 1152 pixels", "ports": {"hdmi": 1, "usb": 3}, "speakers": {"left": "10 watt", "right": "10 watt"}}'),
    ("2", "Amy", "amy", '{"screen": "40 inch", "resolution": "1920 x 1080 pixels", "ports": {"hdmi": 1, "usb": 2}, "speakers": {"left": "10 watt", "right": "10 watt"}}'),
    ("3", "Michael", "michael", '{"screen": "30 inch", "resolution": "1600 x 900 pixles", "ports": {"hdmi": 1, "usb": 1}, "speakers": {"left": "10 watt", "right": "10 watt"}}'),
    ("4", "Hennah", "hennah", '{"screen": "25 inch", "resolution": "1366 x 768 pixels", "ports": {"hdmi": 1, "usb": 0}, "speakers": {"left": "5 watt", "right": "5 watt"}}')
]

## executing the query with values
cursor.executemany(query, values)

## to make final output we have to run the 'commit()' method of the database object
db.commit()

query = "SELECT * FROM txs WHERE addr -> '$.resolution' = '2048 x 1152 pixels';"

## getting records from the table
cursor.execute(query)

## fetching all records from the 'cursor' object
records = cursor.fetchall()

## Showing the data
for record in records:
    print(record)