import serial
import sys
import json
import datetime
from libUtils import mapPath, parseWithTypes, JsonType, fromJson, toJson
from libLogging import buildLogger
from libComms import parseCommPort

def parsePrinterProtocol(jsonNode):
	return parseWithTypes(jsonNode, MarlinPrinterProtocol);
# Sends G-Code & recieves / Interprets Reponses
@JsonType
class MarlinPrinterProtocol:
	def __init__(self, commPort):
		self.mCommPort = commPort;
		self.errors = [];
		self.logger = buildLogger("lib3dPrinter.py->MarlinPrinterProtocol");
	def open(self):
		self.mCommPort.open();
		self.printResponse();
	def close(self):
		self.mCommPort.close();
	def printResponse(self):
		lines = [];
		while True:
			s = self.mCommPort.readline();
			if s == '':
				break;
			lines += [s];
			self.logger.log("From Printer: " + s[:-1]);
			return lines;
	def readUntilOkOrError(self):
		while True:
			s = self.mCommPort.readline();
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
			s = self.mCommPort.readline();
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
		self.logger.logVerbose("Sending Command: " + cmd);
		self.mCommPort.write(cmd + "\n");
		return self.readUntilOkOrError();
	def emergencyStop(self):
		self.logger.log("Sending E-Stop Commands");
		self.sendCmd("M18");
		self.sendCmd("M140 S0");
		self.sendCmd("M104 S0");
		self.sendCmd("M81");
	def toJson(self):
		return {mCommPort=toJson(self.mCommPort));
	@staticmethod
	def fromJson(jsonNode):
		# commPort = None;
		# commPort = commPort if commPort != None else ComPortWrapper.fromJson(mapPath(jsonNode, "commPort"));
		return MarlinPrinterProtocol(
			commPort=fromJson(jsonNode["mCommPort"]);
			);
def parseGcodeBuffer(jsonNode):
	return parseWithTypes(jsonNode, GcodeCommandBuffer);
@JsonType
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
	def toJson(self):
		return { filePath=self.mFilePath, nextCommand=self.mNextCommand };
	@staticmethod
	def fromJson(jsonNode):
		return GcodeCommandBuffer(
			filePath=mapPath(jsonNode, "filePath"),
			startAtCmd=mapPath(jsonNode, "nextCommand", 0)
			);

