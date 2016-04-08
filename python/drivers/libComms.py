import serial
import sys
import json
import datetime
from libUtils import parseWithTypes, mapPath, JsonType
from libLogging import buildLogger

def parseCommPort(jsonNode, loggerFactory):
	ret = parseWithTypes(jsonNode, ComPortWrapper);

@JsonType
class ComPortWrapper:
	def __init__(self, port='/dev/ttyACM0', baud=115200, timeout=0.5):
		self.mPort = port;
		self.mBaud = baud;
		self.mTimeout = timeout;
		self.mHandle = None;
		self.logger = buildLogger("ComPortWrapper");
	def open(self):
		if self.mHandle == None:
			self.close();
		self.mHandle = serial.Serial(self.mPort, self.mBaud, timeout=self.mTimeout);
		return self.mHandle != None;
	def isOpen(self):
		return self.mHandle != None;
	def close(self):
		if self.mHandle != None:
			self.mHandle.close();
	def readline(self):
		if self.mHandle != None:
			return self.mHandle.readline();
		return None;
	def read(self, n=-1):
		if self.mHandle != None:
			return self.mHandle.read(n);
		return None;
	def write(self, s):
		if self.mHandle != None:
			return self.mHandle.write(s);
		else:
			return None;
	def flush(self):
		if self.mHandle != None:
			return self.mHandle.flush();
	def __del__(self):
		self.close();
	def toJson(self):
		return {mBaud=self.mBaud, mPort=self.mPort, mTimeout=self.mTimeout};
	@staticmethod
	def fromJson(jsonNode):
		return ComPortWrapper(
			port=mapPath(jsonNode, "mPort", '/dev/ttyACM0'), 
			baud=mapPath(jsonNode, "mBaud", 115200),
			timeout=mapPath(jsonNode, "mTimeout", 0.5)
			);
@JsonType
class MockComPortWrapper:
	def __init__(self):
		self.imOpen = False;
	def open(self):
		self.imOpen = True;
		return self.imOpen;
	def isOpen(self):
		return self.imOpen;
	def close(self):
		self.imOpen = True;
	def readline(self):
		if self.imOpen:
			return "OK\n";
	def read(self, n=-1):
		return None;
	def write(self, s):
		return len(s);
	def flush(self):
		0;
	def __del__(self):
		0;
	def toJson(self):
		return {};
	@staticmethod
	def fromJson(jsonNode):
		return MockComPortWrapper();

