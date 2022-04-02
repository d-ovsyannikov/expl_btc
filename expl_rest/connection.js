const mysql = require('mysql');

var db = mysql.createConnection({
    host: "localhost",
	// user: "root",
	user: "expl_btc",
    // password: "Gfhjkmgfhjkm3!",
	// database: "datacamp"
	password: "Gfhjkmgfhjkm1",
	database: "expl_btc_db"
})

db.connect((err)=>{
	if (!err)
	{
		console.log("Connected to DB");
	}
	else
	{
		console.log("Connection to DB failed", err.message);
	}
});

module.exports = db;