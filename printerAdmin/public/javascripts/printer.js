

function sendPrinterCommand(cmd, success, failure) {

  var par = { "command": cmd };

  console.log('2');
  $.ajax({
    url: '/gcodeCommand',
    type: "POST",
    data: JSON.stringify(par),
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    success: function (results) {
      console.log('success');
      console.log(results);
      if (success) {
        success(results);
      }
    },
    error: function (error) {
      console.log(error);
      if (failure) {
        console.log('here');
        failure(error);
      }
    }
  })

}

function getGCodeFiles(success, isDev) {
  $.ajax({
    url: '/gcode',
    type: "GET",
    contentType: "application/json; charset=utf-8",
    dataType: "json",

    success: function (results) {
            // console.log(results);
      if (success) {
        success(results);
      }
    },
    error: function (error) {
      console.log(error);
    }
  })
}

function printFile(gcodeFile) {
  var rootURL = 'http://localhost:3000/printGCodeFile';
  var data = { "file": gcodeFile }
  $.ajax({
    url: rootURL,
    type: "POST",
    data: JSON.stringify(data),
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    success: function (msg) {
      console.log('success');
      console.log(msg);
    }
  })
}


function sendHome(success, error) {
  console.log('1');
  sendPrinterCommand('G28', success, error);
}

function heatBed( success, error) {
  sendPrinterCommand('M140 S70', success, error);
}

function turnOffBed() {
  sendPrinterCommand('M140 S0');
}

function heatExtruder() {
  sendPrinterCommand('M104 S219');
}

function turnOffExtruder() {
  sendPrinterCommand('M104 S0');
}

function customGcode(gCode,success, error) {
 console.log(gCode)
 if(gCode){
    sendPrinterCommand(gCode,success, error);
 }

}