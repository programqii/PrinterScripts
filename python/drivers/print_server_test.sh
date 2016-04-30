base_url='http://raspberrypi:8080'
printer_cmd="$base_url"'/api/printer/printer-b9cf5eb3-0846-11e6-b2bd-f45c898f3b77'
echo "Create Job"
job_id=$(curl -X POST "$base_url"'/api/jobs/new' | grep -o 'job-[^"]*')
#job_id='job-020327ba-0e0f-11e6-b091-b827eb0431d7'
echo "JobId: $job_id"
echo "Upload Gcode"
curl -X POST "$base_url"'/api/job/'"$job_id"'/gcode' -F "file=@$1"
echo ""
echo "Stop Printer's current job"
curl -X POST "$printer_cmd"'/start'
echo ""
echo "Assign job to Printer"
curl -X POST "$printer_cmd"'/job' -H 'Content-Type: application/json' -d '{"jobId":"'"$job_id"'"}'
echo ""
echo "Start Printer's current job"
curl -X POST "$printer_cmd"'/start'
echo ""
