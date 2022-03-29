const express = require('express');
const Router = express.Router();
const db = require('../connection')

Router.get("/", (req, res)=>{
	db.query("select * from outs limit 3", (err, rows, fields)=>{
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