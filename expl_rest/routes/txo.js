const express = require('express');
const txoRouter = express.Router();
const db = require('../connection')
const axios = require('axios');

txo_query = {
    method: 'post',
    url: 'http://username:password@127.0.0.1:8332/',
    data: {"jsonrpc": "1.0", "id":"curltest", "method": "gettxout", "params": ["", 0] },
    headers: {
      'Content-Type': 'multipart/form-data'
    }
}

txoRouter.get("/", (req, res)=>{
	console.log(req.query.tx)
    console.log(req.query.n)

    txo_query["data"]["params"][0] = req.query.tx
    txo_query["data"]["params"][1] = parseInt(req.query.n)
    // console.log(query)
	axios(txo_query)    
    .then(btc_res => {
        if (!btc_res.data.result){
            db.query("select * from ins where tx_src='"+req.query.tx+"' and out_ind="+ req.query.n +";", (err, rows, fields)=>{
                if (!err)
                {
                    if (rows.length) {
                        res.send({result: "found", data: rows});
                    } else {
                        res.send({result: "not found"});
                    }
                }
                else
                {
                    console.log(err);
                }
            });
        } else {
            res.send({result: "utxo"});
        }

        // res.send(btc_res.data.result);
        // console.log(`statusCode: ${btc_res.status}`)
        // console.log(btc_res.data.result)
    })
        .catch(error => {
        console.error(error)
    })
})

module.exports = txoRouter;