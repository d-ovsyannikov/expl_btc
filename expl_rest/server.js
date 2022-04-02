const mysql = require('mysql');
const express = require('express')
const bodyParser = require('body-parser')
const db = require('./connection')

const addrRouter = require('./routes/address');
const txRouter = require('./routes/tx');

const app = express()
const port = process.env.PORT || 3500

app.use(bodyParser.json())
app.use('/address', addrRouter);
app.use('/tx', txRouter);

app.listen(port)