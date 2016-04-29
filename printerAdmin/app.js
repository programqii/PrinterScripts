var express = require('express');
var path = require('path');
var favicon = require('serve-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
var http = require('http');
var routes = require('./routes/index');
var users = require('./routes/users');
var serveIndex = require('serve-index');
var glob = require("glob");
var io = require('socket.io')(http);

var app = express();

//var baseURL = '192.168.1.149';
var baseURL = 'localhost';
var basePort = '8081';
app.use(bodyParser.json());

//CORS middleware
var allowCrossDomain = function (req, res, next) {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE');
  res.header('Access-Control-Allow-Headers', 'Content-Type, X-XSRF-TOKEN');
  next();
};

app.use(allowCrossDomain);

app.post('/gcodeCommand', function (req, res) {

    var commandData = JSON.stringify({
    'command': req.body.command
  });

  var extServerOptionsPost = {
    host: baseURL,
    port: basePort,
    path: '/sendRawCommand',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(commandData)
    }
  };


  var reqPost = http.request(extServerOptionsPost, function (resp) {
    console.log("response statusCode: ", res.statusCode);
  	res.on('data', function (data) {
          console.log(data);
    });
   // res.on('data', function (data) {
    //  response.send('POST request to homepage');

      console.log('Posting Result:\n');
      console.log(resp.data);
      //process.stdout.write(data);
      console.log('\n\nPOST Operation Completed');

      var responseOut = {
        status: 200,
        success: 'Updated Successfully'

      };
      res.send(responseOut);

   // });
  });
    reqPost.write(commandData);
  reqPost.end();
});

app.post('/printGCodeFil_old', function (req, res) {
  var fileData = JSON.stringify({
    'file': req.body.file
  });
  console.log(fileData);
});

app.post('/gcodeCommand_old', function (req, res) {

  var commandData = JSON.stringify({
    'command': req.body.command
  });

  var extServerOptionsPost = {
    host: baseURL,
    port: basePort,
    path: '/sendRawCommand',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(commandData)
    }
  };

  var reqPost = http.request(extServerOptionsPost, function (res) {
    console.log("response statusCode: ", res.statusCode);

    res.on('data', function (data) {
      response.send('POST request to homepage');

      console.log('Posting Result:\n');
      process.stdout.write(data);
      console.log('\n\nPOST Operation Completed');
      var response = {
        status: 200,
        success: 'Updated Successfully'
      };

    });
  });
  reqPost.write(commandData);
  reqPost.on('error', function (e) {

    console.error(e);
  });
  // response.send('POST request to homepage');
  reqPost.end();
});

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

// uncomment after placing your favicon in /public
//app.use(favicon(path.join(__dirname, 'public', 'favicon.ico')));
app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));
//app.use(express.directory('public/gCode'));
app.use('/gcode', serveIndex('public/gCode', { 'icons': true }))

app.use('/', routes);
app.use('/users', users);

// catch 404 and forward to error handler
app.use(function (req, res, next) {
  var err = new Error('Not Found');
  err.status = 404;
  next(err);
});

// error handlers

// development error handler
// will print stacktrace
if (app.get('env') === 'development') {
  app.use(function (err, req, res, next) {
    res.status(err.status || 500);
    res.render('error', {
      message: err.message,
      error: err
    });
  });
}

// production error handler
// no stacktraces leaked to user
app.use(function (err, req, res, next) {
  res.status(err.status || 500);
  res.render('error', {
    message: err.message,
    error: {}
  });
});

app.get('/gcode', function (req, res) {
  glob("*.gcode", options, function (er, files) {
    console.log(files);
    // files is an array of filenames.
    // If the `nonull` option is set, and nothing
    // was found, then files is ["**/*.js"]
    // er is an error object or null.
    res.send(files);
  });
  
app.get('/links', function (req, res) {
  res.send('links');
  });
  
});
module.exports = app;
