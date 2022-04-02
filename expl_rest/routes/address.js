const express = require('express');
const Router = express.Router();
const db = require('../connection')

Router.get("/", (req, res)=>{
	console.log(req.query.addr)
	db.query("select * from outs where addr='"+req.query.addr+"';", (err, rows, fields)=>{
		if (!err)
		{
			res.send(rows);
		}
		else
		{
			console.log(err);
		}
	});

})

module.exports =Router;