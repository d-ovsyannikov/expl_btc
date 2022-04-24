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

    txRouter.get("/", async (req, res)=>{
        tx_query["data"]["params"][0] = req.query.tx
        console.log(tx_query)
        const btc_res = await axios(tx_query)    
        if (btc_res) {
            console.log(btc_res)
            // iterate through all in txs
            // btc_res.data.result.vin.forEach(function (value, i) {
            for (const [i, ins] of (btc_res.data.result.vin.entries())){
                console.log( i, ins);
                // console.log(i, ins.txid)
                tx_query["data"]["params"][0] = ins.txid
                const btc_res2 = await axios(tx_query)
                if (btc_res2) {
                    // console.log(btc_res2.data.result)
                    if ("address" in btc_res2.data.result.vout[ins.vout].scriptPubKey){
                        btc_res.data.result.vin[i]["addr"] = btc_res2.data.result.vout[ins.vout].scriptPubKey.address
                    }
                    if ("addresses" in btc_res2.data.result.vout[ins.vout].scriptPubKey){
                        btc_res.data.result.vin[i]["addr"] = btc_res2.data.result.vout[ins.vout].scriptPubKey.addresses[0]
                    }
                    btc_res.data.result.vin[i]["value"] = btc_res2.data.result.vout[ins.vout].value
                }

            }
            
            // console.log(btc_res.data.result)
            res.send(btc_res.data.result);
            // console.log(`statusCode: ${btc_res.status}`)
            // console.log(btc_res.data)
        } else {
            console.error(error)
        }
    })



module.exports = txRouter;