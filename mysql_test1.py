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
cursor.execute("CREATE TABLE txs (id INT(11) NOT NULL PRIMARY KEY, name VARCHAR(255), user_name VARCHAR(255))")

query = "INSERT INTO txs (id, name, user_name) VALUES (%s, %s, %s)"
## storing values in a variable
values = [
    ("1", "Peter", "peter"),
    ("2", "Amy", "amy"),
    ("3", "Michael", "michael"),
    ("4", "Hennah", "hennah")
]

## executing the query with values
cursor.executemany(query, values)

## to make final output we have to run the 'commit()' method of the database object
db.commit()

query = "SELECT * FROM txs"

## getting records from the table
cursor.execute(query)

## fetching all records from the 'cursor' object
records = cursor.fetchall()

## Showing the data
for record in records:
    print(record)

