var express = require('express');
var bodyParser = require('body-parser');
var crud = require('./modules/crud');
var r = require('rethinkdb');

var config = require(__dirname + '/config.js');
var routes = require('./routes/index');
var app = express();

app.use(bodyParser.json());
app.set('views', __dirname + '/views');
app.get('/cruds', crud.findAll);
app.get('/cruds/:id', crud.findById);
app.post('/cruds', crud.create);
app.delete('/cruds:id', crud.delete);
app.put('/cruds:id', crud.update);

app.use('/', routes);

app.listen(config.express.port);

console.log('started...');
