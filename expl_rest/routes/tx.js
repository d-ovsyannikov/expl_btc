const express = require('express');
const axios = require('axios');
const Router = express.Router();

query = {
    method: 'post',
    url: 'http://username:password@127.0.0.1:8332/',
    data: {"jsonrpc": "1.0", "id":"curltest", "method": "getrawtransaction", "params": ["db102946b5971045e213a6f0718f779d7d9bb533f7a4ce66d77c030afa77fc97", true] },
    headers: {
      'Content-Type': 'multipart/form-data'
    }
}

Router.get("/", (req, res)=>{
	console.log(req.query.tx)
    query["data"]["params"][0] = req.query.tx
	axios(query)    
    .then(btc_res => {
        res.send(btc_res.data.result);
        // console.log(`statusCode: ${res.status}`)
        // console.log(res.data.result)
    })
        .catch(error => {
        console.error(error)
    })
})

module.exports = Router;