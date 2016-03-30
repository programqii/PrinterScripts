import serial
import sys

class ArgsParse:
	def  __init__(self):
		self.argMap = {}
		self.flags = [];
		offset = 0;
		for i in sys.argv[1:]:
			offset = i.find("=");
			if offset > -1:
				self.argMap[i[:offset].lower()] = i[offset+1:];
			else:
				self.flags += [i.lower()];
	def hasFlag(self, flagName):
		for i in self.flags:
			if i == flagName.lower():
				return True;
		return False;
	def getValue(self, name, defaultValue):
		if( name.lower() in self.argMap):
			return self.argMap[name.lower()]
		return defaultValue;
class Logger:
	def __init__(self, tag):
		self.tag = tag;
	def log(self, message):
		print(self.tag + ": " + message);
class PrinterProtocol:
	def __init__(self, port='/dev/ttyACM0', baud=115200, timeout=0.5, logger=Logger("PrinterProtocol")):
		self.mPort = port;
		self.mBaud = baud;
		self.mTimeout = timeout;
		self.ser = None;
		self.errors = [];
		self.logger = logger;
	def open(self):
		self.ser = serial.Serial(self.mPort, self.mBaud, timeout=self.mTimeout);
		self.printResponse();
	def close(self):
		if self.ser != None:
			self.ser.close();
	def printResponse(self):
		while True:
			s = self.ser.readline();
			if s == '':
				break;
			self.logger.log("From Printer: " + s[:-1]);
	def readUntilOkOrError(self):
		while True:
			s = self.ser.readline();
			if s.find(":") > -1:
				tag = s[:s.find(":")];
			else:
				tag = "";
			if s.lower() == "ok\n":
				return True;
			if(s != ''):
				self.logger.log("From Printer: " + s[:-1]);
			if tag.lower() == "error":
				return False;
	def readUntilOkOrError(self):
		lines = [];
		while True:
			s = self.ser.readline();
			if s.find(":") > -1:
				tag = s[:s.find(":")];
			else:
				tag = "";
			if s.lower() == "ok\n":
				return {"ok": True, "data": lines};
			if(s != ''):
				lines += [s[:-1] if s[-1:] == "\n" else s];
				self.logger.log("From Printer: " + s[:-1]);
			if tag.lower() == "error":
				return {"ok": False, "data": lines};
	def sendCmd(self, cmd):
		self.logger.log("Sending Command: " + cmd);
		self.ser.write(cmd + "\n");
		return self.readUntilOkOrError();
	def emergencyStop(self):
		self.sendCmd("M18");
		self.sendCmd("M140 S0");
		self.sendCmd("M104 S0");
		self.sendCmd("M81");
class GcodeCommandBuffer:
	def __init__(self, filePath):
		self.mLines = [];
		self.mNextCommand = 0;
		f = open(filePath);
		l = f.readline();
		lineCounter = 1;
		while l != '':
			commentPos = l.find(";");
			comment = None
			if(commentPos > -1):
				comment = l[commentPos+1:].strip();
				l = l[:commentPos];
			l = l.strip();
			if(len(l) > 0 or comment != None):
				self.mLines += [{"cmd":l, "comment":comment, "line":lineCounter}]; 
			lineCounter += 1
			l = f.readline();
		f.close();
	def nextCommand(self):
		if(nextCommand < len(self.mLines)):
			temp = self.mLines[self.mNextCommand];
			self.mNextCommand += 1;
			return temp;
		return {"cmd": "", "comment":"End of commands!!!", "line":-1};
	def percentComplete(self):
		return (1.0*self.mNextCommand) / len(self.mLines);
	def numCommandsLeft(self):
		return len(self.mLines) - self.mNextCommand;


