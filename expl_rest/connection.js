const mysql = require('mysql');

var db = mysql.createConnection({
    host: "localhost",
	user: "root",
    password: "Gfhjkmgfhjkm3!",
	database: "datacamp"
})

db.connect((err)=>{
	if (!err)
	{
		console.log("Connected");
	}
	else
	{
		console.log("Connection failed", err.message);
	}
});

module.exports = db;