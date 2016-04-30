import serial
import sys
import json
import datetime
from libUtils import parseWithTypes, mapPath, JsonType
from libLogging import NullLogger

def parseCommPort(jsonNode, loggerFactory):
	ret = parseWithTypes(jsonNode, ComPortWrapper);

@JsonType(saveThese=["mPort", "mBaud", "mTimeout"])
class ComPortWrapper:
	def __init__(self, port='/dev/ttyACM0', baud=115200, timeout=0.5):
		self.mPort = port;
		self.mBaud = baud;
		self.mTimeout = timeout;
		self.mHandle = None;
		self.logger = NullLogger();
	def setLoggerFactory(self, loggerFactory):
		self.logger = loggerFactory.buildLogger("libComms.py->ComPortWrapper");
		if self.logger == None:
			self.logger = NullLogger();
	def open(self):
		if self.mHandle == None:
			self.close();
		self.logger.logInfo("Opening Serial Port "+ str(self.mPort) + " @ "+ str(self.mBaud) + " baud");
		self.mHandle = serial.Serial(self.mPort, self.mBaud, timeout=self.mTimeout);
		return self.mHandle != None;
	def isOpen(self):
		return self.mHandle != None;
	def close(self):
		if self.mHandle != None:
			self.mHandle.close();
			self.logger.logInfo("Closing Serial Port "+ self.mPort);
	def readline(self):
		if self.mHandle != None:
			return self.mHandle.readline();
		return None;
	def read(self, n=-1):
		if self.mHandle != None:
			resp = self.mHandle.read(n);
			if resp != None:
				resp = resp.decode('utf-8'); #TODO: Verify Encoding on Actual Marlin Hardware
			return resp;
		return None;
	def write(self, s):
		if self.mHandle != None:
			return self.mHandle.write(s.encode('utf-8')); #TODO: Allow for raw binary to be sent?
		else:
			return None;
	def flush(self):
		if self.mHandle != None:
			return self.mHandle.flush();
	def __del__(self):
		self.close();
	# def toJson(self):
	# 	return {"mBaud":self.mBaud, "mPort": self.mPort, "mTimeout":self.mTimeout};
	# @staticmethod
	# def fromJson(jsonNode):
	# 	return ComPortWrapper(
	# 		port=mapPath(jsonNode, "mPort", '/dev/ttyACM0'), 
	# 		baud=mapPath(jsonNode, "mBaud", 115200),
	# 		timeout=mapPath(jsonNode, "mTimeout", 0.5)
	# 		);
@JsonType(saveThese=[])
class MockComPortWrapper:
	def __init__(self):
		self.imOpen = False;
	def setLoggerFactory(self, loggerFactory):
		return ;
	def open(self):
		self.imOpen = True;
		print("MockComPortWrapper: open()")
		return self.imOpen;
	def isOpen(self):
		return self.imOpen;
	def close(self):
		print("MockComPortWrapper: close()")
		self.imOpen = False;
	def readline(self):
		if self.imOpen:
			return "OK\n";
	def read(self, n=-1):
		return None;
	def write(self, s):
		print("MockComPortWrapper: Sent - " + s)
		return len(s);
	def flush(self):
		0;
	def __del__(self):
		0;

