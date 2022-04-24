const express = require('express');
const Router = express.Router();
const db = require('../connection')

Router.get("/", (req, res)=>{
	console.log(req.query.addr)
	// "select * from outs where addr='"+req.query.addr+"';"
	// create temporary table tx1 as (select txid from outs where addr='1F1tAaz5x1HUXrCNLbtMDqcw6o5GNn4xqX');
	// create temporary table tx2 as (select tx_dst from ins join tx1 on ins.tx_src=tx1.txid);
	// select * from tx2;
	// var rows  = await db.query("select * from outs where addr='"+req.query.addr+"';")
	db.query("DROP TABLE IF EXISTS tx1;", (err1, rows1, fields1)=>{
		if (!err1){
			db.query("create temporary table tx1 as (select txid from outs where addr='"+req.query.addr+"');", (err2, rows2, fields2)=>{
				if (!err2)
				{
					db.query("DROP TABLE IF EXISTS tx2;", (err3, rows3, fields3)=>{
						if (!err3)
						{
							db.query("create temporary table tx2 as (select tx_dst from ins join tx1 on ins.tx_src=tx1.txid);", (err4, rows4, fields4)=>{
								if (!err4)
								{
									db.query("select txid from tx1;", (err5, rows5, fields5)=>{
										if (!err5)
										{
											db.query("select txid from tx2;", (err6, rows6, fields6)=>{
												if (!err6)
												{
													res.send(rows5);
													res.send(rows6);
												}
											});
										}
									});
								}
							});
							// res.send(rows3);
						}
					});
				}
			});
		}
	});
		

})

module.exports =Router;