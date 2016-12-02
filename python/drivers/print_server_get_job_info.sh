base_url='http://raspberrypi:8080'
printer_cmd="$base_url"'/api/printer/printer-b9cf5eb3-0846-11e6-b2bd-f45c898f3b77'
echo "Assign job to Printer"
curl -X GET "$printer_cmd"'/job' -H 'Content-Type: application/json'
