const mysql = require('mysql');
const express = require('express')
const bodyParser = require('body-parser')
const db = require('./connection')

const AddrRouter = require('./routes/address');

const app = express()
const port = process.env.PORT || 3500

app.use(bodyParser.json())
app.use('/address', AddrRouter);

app.listen(port)

// , () => {
//     console.log(`App listen on port ${port}`);
// })