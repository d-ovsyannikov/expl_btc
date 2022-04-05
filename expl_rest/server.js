const mysql = require('mysql');
var cors = require('cors')
const express = require('express')
const bodyParser = require('body-parser')
const db = require('./connection')

const addrRouter = require('./routes/addr');
const txRouter = require('./routes/tx');
const txoRouter = require('./routes/txo');

const app = express()
const port = process.env.PORT || 3500

app.use(cors())
app.get('/products/:id', function (req, res, next) {
  res.json({msg: 'This is CORS-enabled for all origins!'})
})

app.use(bodyParser.json())
app.use('/addr', addrRouter);
app.use('/tx', txRouter);
app.use('/txo', txoRouter);

app.listen(port)