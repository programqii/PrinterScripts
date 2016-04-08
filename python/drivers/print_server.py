import json
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
from lib3dPrinter import MarlinPrinterProtocol, GcodeCommandBuffer
from libComms import ComPortWrapper, MockComPortWrapper
from libUtils import *
from libLogging import buildLogger
import re
import socket

args = ArgsParse();

PORT_NUMBER = int(args.getValue("http_port", 8081));

apiHandler = RequestHandler(basePath="");
class RequestHandler:
	def __init__(self, basePath="/"):
		self.mApis = { "_GET" :[], "_POST":[], "_DELETE":[], "_PUT":[]};
		if basePath != "/":
			self.mBasePath = basePath;
		else:
			self.mBasePath = "";
	def handleRequest(self, method, url, body, headers):
		# Trim Off Base Path part
		if len(self.mBasePath) < len(url) and url[:len(self.mBasePath)] == self.mBasePath and self[len(self.mBasePath)]:
			url = url[len(self.mBasePath):];
		else:
			return None;
		# Search for/By Request Method
		if not (("_" + method) in self.mApis):
			return None;
		# Find Path Match
		for endPoint in self.mApis["_" + method]:
			m = endPoint["pathRegex"].match(url) 
			if m:
				return endPoint["pathRegex"].callBack(method, url, body, headers, m);
		return None;
	def endpoint(self, method, urlExpr):
		def decoratorHandler(func):
			self.mApis["_" + method] = self.mApis["_" + method] || [];
			self.mApis["_" + method] += [{"pathRegex":urlExpr, "callBack": func}];
		return decoratorHandler;	
	def addHandler(self, method, urlExpr, func):
		if not (("_" + method) in self.mApis):
			self.mApis["_" + method] = []
		self.mApis["_" + method] += [{
			"pathRegex":urlExpr,
			"callBack": func
		}];

mimeTypes = {
	".json":"application/json",
	".pdf":"application/pdf",
	".txt":"text/plain",
	".zip":"application/zip",
	".xml":"application/xml"
	".svg":"image/svg+xml",
	".tiff":"image/tiff",
	".png":'image/png',
	".html":"text/html",
	".jpg":'image/jpg',
	".gif":'image/gif',
	".js":'application/javascript',
	".css":'text/css',
	".csv":"text/csv",
	".mdown":"text/markdown"
}
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
	return ApiResponse();
@apiHandler.endpoint("POST", "/api/printers/new")
def createPrinter(method, url, body, headers, matchObject):
	return ApiResponse();
@apiHandler.endpoint("GET", "/api/printer/{id}")
def getPrinterInfo(method, url, body, headers, matchObject):
	return ApiResponse();
@apiHandler.endpoint("DELETE", "/api/printer/{id}")
def deletePrinterInfo(method, url, body, headers, matchObject):
	return ApiResponse();
@apiHandler.endpoint("GET", "/api/printer/{id}/ini_config")
def getPrinterConfigAsIni(method, url, body, headers, matchObject):
	return ApiResponse();
@apiHandler.endpoint("POST", "/api/printer/{id}")
def setPrinterInfo(method, url, body, headers, matchObject):
	return ApiResponse();
@apiHandler.endpoint("GET", "/api/printer/{id}/status")
def getPrinterStatus(method, url, body, headers, matchObject):
	return ApiResponse();
@apiHandler.endpoint("POST", "/api/printer/{id}/stop")
def stopPrinter(method, url, body, headers, matchObject):
	return ApiResponse();
@apiHandler.endpoint("POST", "/api/printer/{id}/pause")
def pausePrinter(method, url, body, headers, matchObject):
	return ApiResponse();
@apiHandler.endpoint("POST", "/api/printer/{id}/resume")
def resumePrinter(method, url, body, headers, matchObject):
	return ApiResponse();
@apiHandler.endpoint("POST", "/api/printer/{id}/rawGcode")
def sendRawGcodeToPrinter(method, url, body, headers, matchObject):
	return ApiResponse();

# Info About Varrious Print-Jobs that have been Sceduled
@apiHandler.endpoint("GET", "/api/jobs")
def getJobs(method, url, body, headers, matchObject):
	return ApiResponse();
@apiHandler.endpoint("POST", "/api/jobs")
def newJob(method, url, body, headers, matchObject):
	return ApiResponse();
@apiHandler.endpoint("POST", "/api/job/{id}/stop")
def stopJob(method, url, body, headers, matchObject):
	return ApiResponse();
@apiHandler.endpoint("POST", "/api/job/{id}/pause")
def pauseJob(method, url, body, headers, matchObject):
	return ApiResponse();
@apiHandler.endpoint("POST", "/api/job/{id}/resume")
def resumeJob(method, url, body, headers, matchObject):
	return ApiResponse();
@apiHandler.endpoint("GET", "/api/job/{id}/log")
def resumeJob(method, url, body, headers, matchObject):
	return ApiResponse();
@apiHandler.endpoint("DELETE", "/api/job/{id}")
def deleteJobInfo(method, url, body, headers, matchObject):
	return ApiResponse();

@apiHandler.endpoint("POST", "/api/sendRawCommand")
def sendRawCommand(method, url, body, headers, matchObject):
	response = ApiResponse();
	data = json.loads(body);
	cmdRes = printer.sendCmd(data["command"]);
	res = {"data":cmdRes["data"]};
	response.setCode(200 if cmdRes["ok"] else 500);
	response.setBody(json.dumps(res));
	response.setHeader('Content-type', 'application/json');
	return response;
class ApiResponse:
	def __init__(self, code=500, body="", headers={}):
		self.mBody = body;
		self.mCode = code;
		self.mHeaders = headers;
	def setHeader(self, name, value):
		self.mHeaders[name] = value;
	def setCode(self, code):
		self.mCode = code;
	def setBody(self, body):
		self.mBody = body;
#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	def sendToHandle(self, type):
		response = apiHandler.handleRequest("GET", self.path, self.rfile.read(int(self.headers['content-length'])), self.headers);
		if response != None:
			self.send_response(response.mCode);
			for i in response.mHeaders:
				self.send_header(i, response.mHeaders[i]);
			self.end_headers();
			self.wfile.write(response.mBody);
		else:
			self.send_response(500)
			self.end_headers()
			self.wfile.write("")
			f.close();
	#Handler for the GET requests
	def do_GET(self):
		self.sendToHandle("GET");
	#Handler for the POST requests
	def do_POST(self):
		self.sendToHandle("POST");
	def do_DELETE(self):
		return;		
			
printer = PrinterProtocol(port=port, baud=baud, timeout=0.5);
try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on ' + socket.gethostname() + ":" + str(PORT_NUMBER)
	server.timeout=0.1;
	printer.open();
	printer.printResponse();
	#Wait forever for incoming htto requests
	server.serve_forever();
	# while True:
	# 	server.handle_request();
	# 	print "lol"

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()
	printer.emergencyStop();
	printer.close();