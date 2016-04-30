import sys
import json
import datetime
from libLogging import NullLogger

logger = NullLogger();
class BeginEnd:
	def __init__(self, beginFunc=None, endFunc=None):
		self.mBegin = beginFunc;
		self.mEnd = endFunc;
	def __enter__(self):
		if self.mBegin != None:
			self.mBegin();
	def __exit__(self, pType, pValue, pTraceback):
		if self.mEnd != None:
			self.mEnd();
# Structure & function for registering json "types" that have toJson & fromJson defined
__ClassNames = {};
def JsonType(typeName=None, saveThese=None):			
	def handleClassDef(classDef):
		# Dynamically add toJson/fromJson 
		if saveThese != None:
			if isinstance(saveThese, list):
				def toJson(self):
					ret = {};
					for i in saveThese:
						ret[i] = toJsonMap(getattr(self, i));
					return ret;
				def updateFromJson(self, jsonNode, blackList=[], whiteList=None):
					if whiteList == None:
						whiteList = saveThese;
					for i in saveThese:
						if (i in jsonNode) and (i in whiteList) and (not (i in blackList)):
							setattr(self, i, fromJsonMap(jsonNode[i]));
				@staticmethod
				def fromJson(jsonNode):
					# print ("Reading: " + classDef.__name__)
					ret = classDef();
					for i in saveThese:
						if i in jsonNode:
							setattr(ret, i, fromJsonMap(jsonNode[i]));
					return ret;
				setattr(classDef, "fromJson", fromJson);
				classDef.toJson = toJson;
				classDef.updateFromJson = updateFromJson;
			elif isinstance(saveThese, dict):
				def toJson(self):
					ret = {};
					for i in saveThese:
						ret[saveThese[i]] = getattr(self, i);
					return ret;
				def updateFromJson(self, jsonNode, blackList=[], whiteList=None):
					if whiteList == None:
						whiteList = saveThese;
					for i in saveThese:
						if (i in jsonNode) and (i in whiteList) and (not (i in blackList)):
							setattr(self, i, fromJsonMap(jsonNode[saveThese[i]]));
				@staticmethod
				def fromJson(jsonNode):
					# print ("Reading: " + classDef.__name__)
					ret = classDef();
					for i in saveThese:
						if saveThese[i] in jsonNode:
							setattr(ret, i, fromJsonMap(jsonNode[saveThese[i]]));
					return ret;
				setattr(classDef, "fromJson", fromJson);
				classDef.toJson = toJson;
				classDef.updateFromJson = updateFromJson;
		__ClassNames[typeName or classDef.__name__] = classDef;
		# print("Registered " + classDef.__name__ + " as " + (typeName or classDef.__name__) + " for JsonType");
		return classDef;
	return handleClassDef;

#Python Compat
def rawUserInput(prompt):
	if (sys.version_info > (3, 0)):
		# Python 3 code in this block
		return input(prompt);
	else:
		# Python 2 code in this block
		return raw_input(prompt)

@JsonType(typeName="ArgumentList", saveThese=["argMap", "flags"] )
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
	# @staticmethod
	# def fromJson(jsonNode):
	# 	ret = ArgsParse(argv=[]);
	# 	ret.argMap = mapPath(jsonNode, "argMap", {});
	# 	ret.flags = mapPath(jsonNode, "flags", []);
	# 	return ret;
	# def toJson(self):
	# 	return {"argMap":self.argMap, "flags": self.flags};


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
def parseWithTypes(jsonNode, *args, **margs):
	for i in args:
		r = i.fromJson(jsonNode);
		if r != None:
			return r;
	return margs["defaultValue"] if "defaultValue" in margs else None;

# Recursivly parse Json Structure
def fromJsonMap(m):
	if isinstance(m, list):
		r = [];
		for i in m:
			r += [fromJsonMap(i)];
		return r;
	elif isinstance(m, dict):
		if "__type" in m:
			if m["__type"] in __ClassNames:
				return __ClassNames[m["__type"]].fromJson(m);
			else:
				print ("Cannot Find Class def: " + m["__type"]);
			return m
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
def toJsonString(m):
	return json.dumps(toJsonMap(m), indent=4, separators=(',', ': '), sort_keys=True);
def fromJsonString(m):
	return fromJsonMap(json.loads(m));

__callOnShutdown = [];
def OnShutdown(f):
	global __callOnShutdown;
	__callOnShutdown.append(f);
	return f;
def doShutdown():
	global __callOnShutdown;
	__callOnShutdown.reverse();
	for f in __callOnShutdown:
		f();
	__callOnShutdown = [];
def registerShutdownFunction(f):
	global __callOnShutdown;
	if not (f in __callOnShutdown):
		__callOnShutdown.append(f);
def unregisterShutdownFunction(f):
	global __callOnShutdown;
	if f in __callOnShutdown:
		__callOnShutdown.remove(f);

