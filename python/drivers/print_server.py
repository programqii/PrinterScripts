import json
from os import curdir, sep
from lib3dPrinter import MarlinPrinterProtocol, GcodeCommandBuffer
from libComms import ComPortWrapper, MockComPortWrapper
from libUtils import *
from libPrinterObjects import *
from libHttpUtil import *
import re
import socket

apiHandler = RequestHandler();
#TODO: Put this _private_db in the Main print_server.py file if possible
_dataBase = SimplePrinterDB.create("SimpleDB.json");

def getDataBase():
	return _dataBase;

@apiHandler.endpoint("GET", re.compile(r"/static/(.*)(\?.*)?") )
def handleStaticFiles(method, url, body, headers, matchObject):
	try:
		fileName = matchObject.group(1);
		ext = re.match(r".*(\.[^.]*)", fileName).group(1);
		f = open(sep.join([curdir, "http","static", fileName]) );
		response = ApiResponse(code=200)
		response.setBody(f.read());
		if mimeTypes[ext]:
			response.setHeader('Content-type', mimeTypes[ext]);
		response.setCode(200);
		f.close();
		return response;
	except IOError:
		return ApiResponse(code=404);

#TODO: Build out endpoints
# Info About the *Actual* Spools Of Filament (Amount left, Temp Ovveride, etc.)
@apiHandler.endpoint("GET", "/api/spools")
def getSpoolsList(method, url, body, headers, matchObject):
	return ApiResponse();
@apiHandler.endpoint("POST", "/api/spools/new")
def newSpool(method, url, body, headers, matchObject):
	return ApiResponse();
@apiHandler.endpoint("POST", "/api/spools/{spoolId}")
def updateSpool(method, url, body, headers, matchObject):
	return ApiResponse();
@apiHandler.endpoint("GET", "/api/spools/{spoolId}")
def getSpoolInfo(method, url, body, headers, matchObject):
	return ApiResponse();
@apiHandler.endpoint("DELETE", "/api/spools/{spoolId}")
def deleteSpoolInfo(method, url, body, headers, matchObject):
	return ApiResponse();

# # Info around the places to buy flament and the genreal information about the filament itself
# @apiHandler.endpoint("GET", "/api/spoolManufacturers")
# def getFilamentDealers(method, url, body, headers, matchObject):
# 	return ApiResponse();
# @apiHandler.endpoint("POST", "/api/spoolManufacturers/new")
# def addFilamentDealer(method, url, body, headers, matchObject):
# 	return ApiResponse();
# @apiHandler.endpoint("GET", "/api/spoolManufacturer/{id}")
# def getFilamentDealerInfo(method, url, body, headers, matchObject):
# 	return ApiResponse();
# @apiHandler.endpoint("POST", "/api/spoolManufacturer/{id}")
# def updateFilamentDealerInfo(method, url, body, headers, matchObject):
# 	return ApiResponse();
# @apiHandler.endpoint("DELETE", "/api/spoolManufacturer/{id}")
# def deleteFilamentDealerInfo(method, url, body, headers, matchObject):
# 	return ApiResponse();

# Info About the Specific Printers (Connetions, Jobs being executed, Current Material, etc.)

@apiHandler.endpoint("GET", "/api/printers")
def getPrintersList(method, url, body, headers, matchObject):
	return ApiResponse(code=200, jsonBody=getDataBase().listPrinters());
@apiHandler.endpoint("POST", "/api/printers/new")
def createPrinter(method, url, body, headers, matchObject):
	print "createPrinter"
	return ApiResponse(code=200, jsonBody={"printerId":getDataBase().newPrinter()});
@apiHandler.endpoint("GET", "/api/printer/{id}" )
def getPrinterInfo(method, url, body, headers, matchObject):
	printer = getDataBase().getPrinter(matchObject.group(1));
	if printer != None:
		return ApiResponse(code=200, jsonBody=printer);
	else:
		return errorMessageResponse(404, "Cannot find printer \"{0}\"".format(matchObject.group(1)));
@apiHandler.endpoint("DELETE", "/api/printer/{id}")
def deletePrinterInfo(method, url, body, headers, matchObject):
	printer = getDataBase().getPrinter(matchObject.group(1));
	if printer == None:
		return errorMessageResponse(404, "Cannot find printer \"{0}\"".format(matchObject.group(1)));
	elif printer.getCurrentJob() != None:
		return errorMessageResponse(500, "Cannot delete printer \"{0}\" because it is currently assigned job \"{1}\"".format(matchObject.group(1), printer.currentJobId));
	else:
		getDataBase().deletePrinter(matchObject.group(1));
		return ApiResponse(code=200);
# @apiHandler.endpoint("GET", "/api/printer/{id}/ini_config")
# def getPrinterConfigAsIni(method, url, body, headers, matchObject):
# 	return ApiResponse();

@apiHandler.endpoint("POST", "/api/printer/{id}/job")
def setPrinterInfo(method, url, body, headers, matchObject):
	data = fromJsonString(body);
	printer = getDataBase().getPrinter(matchObject.group(1));
	job = getDataBase().getJob(data["jobId"]) if "jobId" in data else None;
	if printer == None:
		return errorMessageResponse(404, "Cannot find printer \"{0}\"".format(matchObject.group(1)));
	elif printer.currentJobId != None:
		return errorMessageResponse(500, "Cannot assign job to printer \"{0}\" because it is currently assigned job \"{1}\" which must be stopped first".format(matchObject.group(1), printer.currentJobId));
	elif not ("jobId" in data):
		return errorMessageResponse(500, "Missing 'jobId' in request");
	elif job == None:
		return errorMessageResponse(404, "Cannot find Job \"{0}\"".format(data["jobId"]));
	else:
		printer.currentJobId = data["jobId"]; #TODO: if job was has already been executed OR job is being executed on another printer -> Copy Job and return a new ID
		job.printerId = matchObject.group(1);
		return ApiResponse(code=200, jsonBody={"jobId": data["jobId"]});
@apiHandler.endpoint("GET", "/api/printer/{id}/job")
def setPrinterInfo(method, url, body, headers, matchObject):
	printer = getDataBase().getPrinter(matchObject.group(1));
	if printer == None:
		return errorMessageResponse(404, "Cannot find printer \"{0}\"".format(matchObject.group(1)));
	elif printer.currentJobId == None:
		return errorMessageResponse(404, "No Job assigned to printer \"{0}\"".format(matchObject.group(1)));
	else:
		printer.currentJobId = data["jobId"]; #TODO: if job was has already been executed OR job is being executed on another printer -> Copy Job and return a new ID
		job.printerId = matchObject.group(1);
		return ApiResponse(code=200, jsonBody={"jobId": printer.currentJobId, "job":printer.getCurrentJob()});
@apiHandler.endpoint("GET", "/api/printer/{id}/status")
def getPrinterStatus(method, url, body, headers, matchObject):
	statusObj = {
		"connected":False, # If the PI is currently connected to printer via Serial
		"state":"Idle" #One of "Idle", "Job Ready"(job assigned but not started), "Running", "Paused", "Off", "Error", etc.
	}
	return ApiResponse(200, jsonBody=statusObj);
@apiHandler.endpoint("POST", "/api/printer/{id}/start")
def getPrinterStatus(method, url, body, headers, matchObject):
	printerId = matchObject.group(1);
	printer = _dataBase.getPrinter(printerId);
	if printer == None:
		return errorMessageResponse(500, "Cannot Find Printer With Id \"{0}\"".format(printerId))
	elif printer.getCurrentJob() == None:
		return errorMessageResponse(500, "No Job Currently Assigned to printer \"{0}\"".format(printerId))
	if printer.startJob():
		return ApiResponse(200, jsonBody={"jobId": printer.currentJobId, "job":printer.getCurrentJob()});
	else:
		return errorMessageResponse(500, "Error Starting Job (Please Check Logs)".format(printerId))
@apiHandler.endpoint("POST", "/api/printer/{id}/stop")
def stopPrinter(method, url, body, headers, matchObject):
	printerId = matchObject.group(1);
	printer = _dataBase.getPrinter(printerId);
	if printer == None:
		return errorMessageResponse(500, "Cannot Find Printer With Id \"{0}\"".format(printerId))
	elif printer.getCurrentJob() == None:
		return errorMessageResponse(500, "No Job Currently Assigned to printer \"{0}\"".format(printerId))
	if printer.stopJob():
		return ApiResponse(200, jsonBody={"jobId": printer.currentJobId, "job":printer.getCurrentJob()});
	else:
		return errorMessageResponse(500, "Error Stopping Job (Please Check Logs)".format(printerId))
@apiHandler.endpoint("POST", "/api/printer/{id}/pause")
def pausePrinter(method, url, body, headers, matchObject):
	printerId = matchObject.group(1);
	printer = _dataBase.getPrinter(printerId);
	if printer == None:
		return errorMessageResponse(500, "Cannot Find Printer With Id \"{0}\"".format(printerId))
	elif printer.getCurrentJob() == None:
		return errorMessageResponse(500, "No Job Currently Assigned to printer \"{0}\"".format(printerId))
	if printer.pauseJob():
		return ApiResponse(200, jsonBody={"jobId": printer.currentJobId, "job":printer.getCurrentJob()});
	else:
		return errorMessageResponse(500, "Error Pausing Job (Please Check Logs)".format(printerId))
@apiHandler.endpoint("POST", "/api/printer/{id}/rawGcode")
def sendRawGcodeToPrinter(method, url, body, headers, matchObject):
	data = fromJsonString(body);
	printer = getDataBase().getPrinter(matchObject.group(1));
	if printer == None:
		return errorMessageResponse(404, "Cannot find printer \"{0}\"".format(matchObject.group(1)));
	# elif printer.getCurrentJob() != None:
	# 	return errorMessageResponse(500, "Cannot Execute G-Code, printer is currently assigned job \"{1}\" which must be stopped first".format(printer.currentJobId));
	elif not ("gcode" in data) and isinstance(data["gcode"], list):
		return errorMessageResponse(500, 'Bad Request body, must have a format of: {"gcode":["Gcode Line1", "Gcode Line 2", ... ]}');
	elif printer.commProtocol == None:
		return errorMessageResponse(500, "Printer Not Properly Set up: commProtocol == None");
	else:
		responseFromPrinter = []; #Note: Need to Make this more Async/Non-Blocking to other threads/Requests
		linesExecuted = 0;
		for i in data["gcode"]:
			linesExecuted += 1;
			gcodeResponse = printer.commProtocol.sendCmd(i);
			responseFromPrinter += gcodeResponse["data"];
			if not gcodeResponse["ok"]:
				return ApiResponse(200, jsonBody={"printerResponse":responseFromPrinter, "ok":False, "linesExecuted": linesExecuted});
		return ApiResponse(200, jsonBody={"printerResponse":responseFromPrinter, "ok":True, "linesExecuted": linesExecuted});
@apiHandler.endpoint("POST", "/api/printer/{id}")
def setPrinterInfo(method, url, body, headers, matchObject):
	response = ApiResponse();
	printer = getDataBase().getPrinter(matchObject.group(1));
	if printer == None:
		return errorMessageResponse(404, "Cannot find printer \"{0}\"".format(matchObject.group(1)));
	elif printer.getCurrentJob() != None:
		return errorMessageResponse(500, "Cannot update printer \"{0}\" because it is currently assigned job \"{1}\"".format(matchObject.group(1), printer.currentJobId));
	else:
		printer.updateFromJson(json.loads(body), blackList=["currentJobId"]); # Do Not allow the assignemnt of jobs through this endpoint 
		return ApiResponse(code=200, jsonBody=printer);

# Info About Varrious Print-Jobs that have been Sceduled
@apiHandler.endpoint("GET", "/api/jobs")
def getJobs(method, url, body, headers, matchObject):
	return ApiResponse(code=200, jsonBody=getDataBase().listJobs());
@apiHandler.endpoint("POST", "/api/jobs/new")
def newJob(method, url, body, headers, matchObject):
	return ApiResponse(code=200, jsonBody={"jobId":getDataBase().newJob()});
# @apiHandler.endpoint("POST", "/api/job/{id}/start")
# def stopJob(method, url, body, headers, matchObject):
# 	return ApiResponse();
# @apiHandler.endpoint("POST", "/api/job/{id}/stop")
# def stopJob(method, url, body, headers, matchObject):
# 	return ApiResponse();
# @apiHandler.endpoint("POST", "/api/job/{id}/pause")
# def pauseJob(method, url, body, headers, matchObject):
# 	return ApiResponse();
# @apiHandler.endpoint("POST", "/api/job/{id}/resume")
# def resumeJob(method, url, body, headers, matchObject):
# 	return ApiResponse();
@apiHandler.endpoint("GET", "/api/job/{id}/log")
def getJobLog(method, url, body, headers, matchObject):
	return ApiResponse();
@apiHandler.endpoint("POST", "/api/job/{id}/gcode") #Submit GCode To Job
def setJobGcode(method, url, body, headers, matchObject):
	job = _dataBase.getJob(matchObject.group(1));
	fileName= "./gcode/forJob-" + matchObject.group(1) +".gcode"
	if job == None:
		return errorMessageResponse(404, "Cannot find Job {0}".format(matchObject.group(1)));

	contentType = headers["content-type"].split(';')[0];
	if(contentType == "application/json"):
		data = json.loads(body);
		if "rawData" in data:
			with open(fileName, "w" ) as f:
				f.write(data["rawData"]);
				job.gcodeFilePath = fileName;
				return ApiResponse(code=200)
		elif "gcodeList" in data:
			with open(fileName, "w" ) as f:
				for g in data["gcodeList"]:
					f.write(g + "\n");
				job.gcodeFilePath = fileName;
				return ApiResponse(code=200);
	elif (contentType == "application/x-www-form-urlencoded"):
		with open(fileName, "w" ) as f:
			f.write(body); #TODO: properly Decode this to recieve a file
			job.gcodeFilePath = fileName;
			return ApiResponse(code=200);
	elif (contentType == "multipart/form-data"):
		data = parseFormData(body, headers);
		if data != None:
			if "file" in data:
				with open(fileName, "w" ) as f:
					f.write(data["file"]["data"]);
					job.gcodeFilePath = fileName;
					return ApiResponse(code=200);
			else:
				return errorMessageResponse(500, "Missing 'file' parameter")
		else:
			return errorMessageResponse(500, "Could Not parse Form")
	return errorMessageResponse(500, "Unrecognized Parameters");
@apiHandler.endpoint("DELETE", "/api/job/{id}")
def deleteJobInfo(method, url, body, headers, matchObject):
	return ApiResponse(code=(200 if getDataBase().deleteJob() else 500));

# Main Program Loop			
def main(args):
	PORT_NUMBER = int(args.getValue("http_port", 8080));
	try:
		#Create a web server and define the handler to manage the
		#incoming request
		server = buildHttpServer(apiHandler=apiHandler, port=PORT_NUMBER);
		# server = HTTPServer(('', PORT_NUMBER), myHandler)
		print 'Started httpserver on ' + socket.gethostname() + ":" + str(PORT_NUMBER)
		server.timeout=0.1;
		#Wait forever for incoming htto requests
		server.serve_forever();
		# while True:
		# 	server.handle_request();
		# 	print "lol"

	except KeyboardInterrupt:
		print '^C received, shutting down the web server'
		server.socket.close()
		doShutdown();
		_dataBase.shutdown();
		# printer.emergencyStop();
		# printer.close();

if __name__ == "__main__":
	main(ArgsParse());