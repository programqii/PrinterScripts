$(document).ready(function () {

  function gCodeFilesCallback(files) {
    var $table = $('#gCodeFilesTable');
    var tbody = $('#tbody');
    for (var i = 0; i < files.length; i++) {
      // create an <tr> element, append it to the <tbody> and cache it as a variable:
      var tr = $('<tr/>').appendTo(tbody);
      tr.append('<td>' + files[i] + '</td><td><button data-action="print-file" rel= ' + files[i] + ' id="' + files[i] + '_button" class="btn-small primary Send print">Print</button></td>');
    }
  }

  var gCodeFiles = getGCodeFiles(gCodeFilesCallback, getUrlVars()["isDev"]);

  $('#autoHome').click(function () {
        showInfoBox('Sending Home', 'info');
    function errorCallback(error) {
      console.log(error);
            showInfoBox('Error- Is printer connected?', 'alert');
    }

    function successCallback(msg) {
      console.log(msg);
      $("#status").html('Sending Home-Success');
    }
    sendHome(successCallback, errorCallback);
  })

  $('#heatBed').click(function () {
    showInfoBox('Heating Bed', 'info');
    function errorCallback(error) {
      console.log(error);
      showInfoBox('Error- Is printer connected?', 'alert');
    }

    function successCallback(msg) {
      console.log(msg);
      showInfoBox('Heating Bed - Success', 'info');
    }

    heatBed(successCallback, errorCallback);
  })

  $('#bedOff').click(function () {
    turnOffBed(getUrlVars()["isDev"]);
  })

  $('#heatExtruder').click(function () {
    heatExtruder(getUrlVars()["isDev"]);
  })

  $('#extruderOff').click(function () {
    turnOffExtruder(getUrlVars()["isDev"]);
  })

  $("button.print").live("click", function () {
    var file = $(this).attr('rel');
    alert(file);
  });

   $('#Gcode').click(function () {
     var gCode = $('#gCode').val();
    showInfoBox('Sending Gcode ' + gCode, 'info');
    function errorCallback(error) {
      console.log(error);
      showInfoBox('Error- Is printer connected?', 'alert');
    }

    function successCallback(msg) {
      console.log(msg);
       showInfoBox('Sending Gcode ' + gCode + ' - Success', 'info');
    }
    
    customGcode(gCode,successCallback, errorCallback);
  })

});

function showInfoBox(text, infoType) {
    $("#status").html(text);
    if (infoType === 'info') {
        $("#status").addClass('info');
    } else {
        $("#status").addClass('alert');
    }
}

function getUrlVars() {
    var vars = [], hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for (var i = 0; i < hashes.length; i++) {
        hash = hashes[i].split('=');
        vars.push(hash[0]);
        vars[hash[0]] = hash[1];
    }
    return vars;
}