import json
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
from Printer3DLib import *
args = ArgsParse();

baud = args.getValue("baud", 115200);
port = args.getValue("port", '/dev/ttyACM0');
#port = args.getValue("port", '/dev/tty.usbmodem1411'); #mac serial port

PORT_NUMBER = int(args.getValue("http_port", 8081));


#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):
		if self.path=="/":
			self.path="/index.html"

		try:
			#Check the file extension required and
			#set the right mime type

			sendReply = False
			if self.path.endswith(".html"):
				mimetype='text/html'
				sendReply = True
			if self.path.endswith(".jpg"):
				mimetype='image/jpg'
				sendReply = True
			if self.path.endswith(".gif"):
				mimetype='image/gif'
				sendReply = True
			if self.path.endswith(".js"):
				mimetype='application/javascript'
				sendReply = True
			if self.path.endswith(".css"):
				mimetype='text/css'
				sendReply = True

			if sendReply == True:
				#Open the static file requested and send it
				f = open(curdir + sep + self.path) 
				self.send_response(200)
				self.send_header('Content-type',mimetype)
				self.end_headers()
				self.wfile.write(f.read())
				f.close()
			return

		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)

	#Handler for the POST requests
	def do_POST(self):
		if self.path=="/sendRawCommand":
			data = json.loads(self.rfile.read(int(self.headers['content-length'])));
			cmdRes = printer.sendCmd(data["command"].encode('ascii'));
			res = {"data":cmdRes["data"]};
			self.send_response(200 if cmdRes["ok"] else 500);
			self.end_headers()
			self.wfile.write(json.dumps(res));
			return			
			
printer = PrinterProtocol(port=port, baud=baud, timeout=0.5);
try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER
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