from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from libUtils import toJsonString, fromJsonString
import re
import json
mimeTypes = {
	".json":"application/json",
	".pdf":"application/pdf",
	".txt":"text/plain",
	".zip":"application/zip",
	".xml":"application/xml",
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
# Example Post Data
# (POST)Match: POST /api/job/{id}/gcode
# Request Headers: 
# 	content-length == 348
# 	accept == */*
# 	user-agent == curl/7.43.0
# 	host == localhost:8080
# 	expect == 100-continue
# 	content-type == multipart/form-data; boundary=------------------------4f74c8d07acdd453
# Request body: 
# --------------------------4f74c8d07acdd453
# Content-Disposition: form-data; name="file"; filename="test.gcode"
# Content-Type: application/octet-stream
#
# ; Test Gcode File to send to server
# ; ANother Line
# --------------------------4f74c8d07acdd453
# Content-Disposition: form-data; name="param2"
#
# p
# --------------------------4f74c8d07acdd453--
def parseFormData(body, headers):
	if headers["content-type"].split(';')[0] != "multipart/form-data":
		return None;
	boundry = headers["content-type"].split('; boundary=')[1];
	ret = {}
	l = body.split("--" +boundry)[1:-1];
	for m in l: #Beginning Should be "" and ending should be "--"
		i = m[2:-2]
		contentStart = re.search(r'\r\n\r\n', i).start() + 2;
		name = "";
		headers = {};
		for k in i[:(contentStart-2)].split("\r\n"): #Header Lines
			headerName = re.match(r'[^:]*: ', k).group(0)[:-2];
			print ("Found Header: " + headerName)
			headers[headerName] = k[(len(headerName) +2):];
			if headerName == "Content-Disposition":
				for m in k[(len(headerName) +2):].split("; ")[1:]:
					if m.split("=")[0] == "name":
						name = m.split("=")[1][1:-1]; #removes quotes as well
						ret[name] = {"data": i[contentStart:], "headers": headers};
	# Ex: {"file": {"data": "Actual Value from Form", "headers":{"Content-Disposition":"form-data", "Content-Type":"application/octet-stream"}}}
	return ret;
def errorMessageResponse(code, errorMessage):
	return ApiResponse(code=code, jsonBody={"errorMessage": errorMessage });

class ApiResponse:
	def __init__(self, code=500, body="", headers={}, jsonBody=None):
		self.mBody = body;
		self.mCode = code;
		self.mHeaders = headers;
		if jsonBody != None:
			self.mHeaders['Content-type'] = 'application/json';
			self.mBody = toJsonString(jsonBody);
	def setHeader(self, name, value):
		self.mHeaders[name] = value;
	def setCode(self, code):
		self.mCode = code;
	def setBody(self, body):
		self.mBody = body;

class RequestHandler:
	def __init__(self, basePath="/"):
		self.mApis = { "GET" :[], "POST":[], "DELETE":[], "PUT":[]};
		if basePath != "/":
			self.mBasePath = basePath;
		else:
			self.mBasePath = "";
	def handleRequest(self, method, url, body, headers):
		# Trim Off Base Path part
		if len(self.mBasePath) < len(url) and url[:len(self.mBasePath)] == self.mBasePath:
			url = url[len(self.mBasePath):];
		else:
			return None;
		# Search for/By Request Method
		if not method in self.mApis:
			return None;
		# Find Path Match
		for endPoint in self.mApis[method]:
			m = endPoint["pathRegex"].match(url) 
			if m:
				print ("(" + method +")Match: "  + endPoint["method"] + " " + endPoint["urlExpr"])
				print ("Request Headers: ");
				for i in headers:
					print ("\t" + i + " == " + headers[i]);
				if body != None:
					if len(body) < 500:
						print ("Request body: ");
						print (body)
					else:
						print ("Request body Size: " + str(len(body)) + " Bytes");				
				return endPoint["callBack"](method, url, body, headers, m);
		return None;
	def endpoint(self, method, urlExpr):
		if isinstance(urlExpr, str):
			Regex = re.sub(r'\{[^}]*\}', r'([^/][^/]*)', urlExpr);
			# print (method+ " Endpoint Regex: " + Regex );
			pathRegex = re.compile('^'+Regex+'$');
		else:
			pathRegex = urlExpr;
		def decoratorHandler(func): #TODO: Incorporate "Key Names" so that the URL Can retrun a Map of Path variables
			self.mApis[method] = self.mApis[method] if method in self.mApis else [];
			self.mApis[method] += [{"pathRegex":pathRegex, "callBack": func, "urlExpr":urlExpr if isinstance(urlExpr, str) else func.__name__, "method": method}];
		return decoratorHandler;	
	def addHandler(self, method, urlExpr, func):
		if not (("_" + method) in self.mApis):
			self.mApis["_" + method] = []
		self.mApis["_" + method] += [{
			"pathRegex":urlExpr,
			"callBack": func
		}];

#This class will handles any incoming request from
#the browser 
def buildHttpServer(apiHandler, port=8080):
	class myHttpHandler(BaseHTTPRequestHandler):
		def sendToHandle(self, pType):
			response = apiHandler.handleRequest(pType, self.path, self.rfile.read(int(self.headers['content-length'])) if 'content-length' in self.headers else "", self.headers);
			if response != None:
				self.send_response(response.mCode);
				for i in response.mHeaders:
					self.send_header(i, response.mHeaders[i]);
				self.end_headers();
				self.wfile.write(response.mBody.encode('utf-8'));
			else:
				print ("No Matching Handler/Endpoint")
				self.send_response(500)
				self.end_headers()
				self.wfile.write("")
				
		#Handler for the GET requests
		def do_GET(self):
			print("do_GET")
			self.sendToHandle("GET");
		#Handler for the POST requests
		def do_POST(self):
			print("do_POST")
			self.sendToHandle("POST");
		def do_DELETE(self):
			print("do_DELETE")
			self.sendToHandle("DELETE");
			return;	
	return HTTPServer(('', port), myHttpHandler);
