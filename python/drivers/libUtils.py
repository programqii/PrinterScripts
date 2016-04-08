import serial
import sys
import json
import datetime
from lib3dPrinter import MarlinPrinterProtocol, GcodeCommandBuffer
from libComms import ComPortWrapper, MockComPortWrapper
from libLogging import buildLogger

logger = buildLogger("libUtils.py");

def rawUserInput(prompt):
	if (sys.version_info > (3, 0)):
		# Python 3 code in this block
		return input(prompt);
	else:
		# Python 2 code in this block
		return raw_input(prompt)

@JsonType("ArgumentList")
class ArgsParse:
	def  __init__(self, argv=None):
		self.argMap = {}
		self.flags = [];
		offset = 0;
		argv = argv if argv != None else sys.argv;
		for i in argv[1:]:
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
	@staticmethod
	def fromJson(jsonNode):
		ret = ArgsParse(argv=[]);
		ret.argMap = mapPath(jsonNode, "argMap", {});
		ret.flags = mapPath(jsonNode, "flags", []);
		return ret;
	def toJson(self):
		return {argMap=self.argMap, flags=self.flags};

def printerFromArgs(args): #Note "args" is an instance of ArgsParse
	global logger;
	baud = args.getValue("baud", 115200);
	port = args.getValue("port", '/dev/ttyACM0');
	timeout = args.getValue("timeout", 1.0);
	useMock = args.getValue("useMock", "False").lower() == "true";
	if(filePath == None and not useMock):
		logger.logError("no File specified");
		exit(1);
	logger.logInfo("Params: port=" + port + ", baud=" + str(baud) + ", File=" + str(filePath)+ ", useMock=" + str(useMock));
	commPort = None;
	if useMock:
		commPort = MockComPortWrapper();
	else:
		commPort = ComPortWrapper(port=port, baud=baud, timeout=timeout);
	return MarlinPrinterProtocol(commPort=commPort )


# Utility Function For Navigating Json Objects more Easily 
def mapPath(mmap, path, defaultValue=None):
	if path=="" or path == None or mmap== None:
		return mmap;
	m = mmap;
	try:
		for i in path.split("/"):
			if i in m:
				m = m[i];
			else:
				return defaultValue;
	except TypeError:
		return defaultValue;
# Try to parse jsonNode with the types listed in args, if unsucccessful, return defaultValue
def parseWithTypes(jsonNode, *args, defaultValue=None):
	for i in args:
		r = i.fromJson(jsonNode);
		if r != None:
			return r;
	return defaultValue;

# Structure & function for registering json "types" that have toJson & fromJson defined
__ClassNames = {};
def JsonType(typeName=None):
	def handleClassDef(classDef):
		__ClassNames[typeName or classDef.__name__] = classDef;
	return handleClassDef;
# Recursivly parse Json Structure
def fromJsonMap(m):
	if isinstance(m, list):
		r = [];
		for i in m:
			r += [fromJsonMap(i)];
		return r;
	elif isinstance(m, dict):
		if "__type" in m and m["__type"] in __ClassNames:
			return __ClassNames[m["__type"]].fromJson(m);
		else:
			r = {};
			for i in m:
				r[i] = fromJsonMap(m[i]);
			return r;
	else:
		return m;
def toJsonMap(m):
	for i in __ClassNames:
		if isinstance(m, __ClassNames[i]):
			m = m.toJson();
			m["__type"] = i;
			return m;
	if isinstance(m, list):
		r = [];
		for i in m:
			r += [toJsonMap(i)];
		return r;
	elif isinstance(m, dict):
		r = {};
		for i in m:
			r[i] = toJsonMap(m[i]);
		return r;
	else:
		return m;
