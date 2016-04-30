import sys
import json
import datetime
from libUtils import mapPath, parseWithTypes, JsonType
from libComms import parseCommPort, ComPortWrapper

def parsePrinterProtocol(jsonNode):
	return parseWithTypes(jsonNode, MarlinPrinterProtocol);
# Sends G-Code & recieves / Interprets Reponses
@JsonType(saveThese=["mCommPort"])
class MarlinPrinterProtocol:
	def __init__(self, commPort=None):
		self.mCommPort = commPort;
		self.errors = [];
		self.logger = None;
	def _log(self, text):
		if self.logger != None:
			self.logger(text);
	def setLoggerFactory(self, loggerFactory):
		self.logger = loggerFactory.buildLogger("lib3dPrinter.py->MarlinPrinterProtocol");
		if self.mCommPort != None:
			self.mCommPort.setLoggerFactory(loggerFactory);
	def isOpen(self):
		if self.mCommPort != None:
			return self.mCommPort.isOpen();
		else:
			return False;
	def open(self):
		if self.mCommPort != None:
			self.mCommPort.open();
			self.printResponse();
			self.sendCmd("M105"); # Read Current Temp (to make sure that The Serial Buffer is clean)
	def close(self):
		if self.mCommPort != None:
			self.mCommPort.close();
	def printResponse(self):
		lines = [];
		if self.mCommPort == None:
			return [];
		while True:
			s = self.mCommPort.readline();
			if s == '':
				break;
			lines += [s];
			self._log("From Printer: " + s[:-1]);
			return lines;
	def readUntilOkOrError(self):
		lines = [];
		if self.mCommPort == None:
			return {"ok": False, "data": lines}
		while True:
			s = self.mCommPort.readline();
			if s.find(":") > -1:
				tag = s[:s.find(":")];
			else:
				tag = "";
			if s.lower() == "ok\n":
				return {"ok": True, "data": lines};
			if(s != ''):
				lines += [s[:-1] if s[-1:] == "\n" else s];
				self._log("From Printer: " + s[:-1]);
			if tag.lower() == "error":
				return {"ok": False, "data": lines};
	def sendCmd(self, cmd):
		if self.mCommPort != None:
			self._log("Sending Command: " + cmd);
			self.mCommPort.write(cmd + "\n");
		return self.readUntilOkOrError();

	def emergencyStop(self):
		self._log("Sending E-Stop Commands");
		self.sendCmd("M18");
		self.sendCmd("M140 S0");
		self.sendCmd("M104 S0");
		self.sendCmd("M81");

def parseGcodeBuffer(jsonNode):
	return parseWithTypes(jsonNode, GcodeCommandBuffer);

@JsonType(saveThese={"filePath": "mFilePath", "nextCommand": "mNextCommand"})
class GcodeCommandBuffer:
	def __init__(self, filePath, startAtCmd=0):
		self.mLines = [];
		self.mNextCommand = startAtCmd;
		self.mFilePath = filePath;
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

