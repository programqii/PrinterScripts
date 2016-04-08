import json

__ClassNames = {};
def JsonType(typeName=None):
	def handleClassDef(classDef):
		__ClassNames[typeName or classDef.__name__] = classDef;
	return handleClassDef;
def fromJsonMap(m):
	if isinstance(m, list):
		r = [];
		for i in m:
			r += [fromJsonMap(i)];
		return r;
	elif isinstance(m, dict):
		if "type" in m and m["type"] in __ClassNames:
			return __ClassNames[m["type"]].fromJson(m);
		else:
			r = {};
			for i in m:
				r[i] = fromJsonMap(m[i]);
			return r;
	else:
		return m;
		
# class Json:
# 	def __init__(self, rootObject={}):
# 		self.rootObject = rootObject;
# 	def __str__(self):
# 		return json.dumps(self.asMap());
# 	def asMap(self):
# 		if isinstance(self.rootObject, list):
# 			m = [];
# 			for i in self.rootObject:
# 				m += [Json(i).asMap()];
# 			return m;
# 		elif isinstance(self.rootObject, dict):
# 			m = {};
# 			for i in self.rootObject:
# 				m[i] = Json(self.rootObject[i]).asMap();
# 			return m;
# 		else:
# 			for i in __ClassNames:
# 				if isinstance(self.rootObject, __ClassNames[i]):
# 					m = self.rootObject.toJson();
# 					m["type"] = i;
# 					return m;
# 			return self.rootObject;
# 	def get(self, path, defaultValue=None):
# 		if path=="" or path == None or self.rootObject == None:
# 			return self;
# 		m = self.rootObject;
# 		try:
# 			for i in path.split("/"):
# 				if i in m:
# 					m = m[i];
# 				else:
# 					return defaultValue;
# 		except TypeError:
# 			return defaultValue;
# 	def contains(self, path):
# 		if path=="" or path == None:
# 			return True;
# 		elif self.rootObject == None:
# 			return False;
# 		m = self.rootObject;
# 		try:
# 			for i in path.split("/"):
# 				if i in m:
# 					m = m[i];
# 				else:
# 					return False;
# 		except TypeError:
# 			return False;
# 		return True;
# 	def set(self, path, value):
# 		m = self.rootObject;
# 		if m == None or path == "/" or path == "":
# 			return;
# 		try:
# 			p = path.split("/");
# 			for i in p[:-1]:
# 				if i in m:
# 					m = m[i];
# 				else:
# 					m[i] = {};
# 					m = m[i];
# 			m[p[-1]] = value;
# 		except TypeError:
# 			return;
# 	def __getitem__(self, index):
# 		if index in self.rootObject:
# 			return self.rootObject;
# 		return None;
# 	def __setitem__(self, index, value):
# 		return self.rootObject.__setitem__(index, value);
# 	def __delitem__(self, index):
# 		return self.rootObject.__delitem__(index);
# 	def __contains__(self, index):
# 		return self.rootObject.__contains__(index);
# 	def __iter__(self):
# 		return self.rootObject.__iter__();