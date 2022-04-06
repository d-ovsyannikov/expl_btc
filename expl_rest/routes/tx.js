const express = require('express');
const axios = require('axios');
const txRouter = express.Router();

tx_query = {
    method: 'post',
    url: 'http://username:password@127.0.0.1:8332/',
    data: {"jsonrpc": "1.0", "id":"curltest", "method": "getrawtransaction", "params": ["", true] },
    headers: {
      'Content-Type': 'multipart/form-data'
    }
}

txRouter.get("/", (req, res)=>{
    tx_query["data"]["params"][0] = req.query.tx
    // console.log(query)
	axios(tx_query)    
    .then(btc_res => {
        res.send(btc_res.data.result);
        // console.log(`statusCode: ${btc_res.status}`)
        // console.log(btc_res.data)
    })
        .catch(error => {
        console.error(error)
    })
})

module.exports = txRouter;