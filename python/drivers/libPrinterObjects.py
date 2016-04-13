from uuid import uuid1 as uuid
from libUtils import *
from libVec import vec
import json

# simple_db = {
# 	"printers":{},
# 	"spools":{},
# 	"spoolManufacturers":{},
# 	"jobs":{}
# };
@JsonType(saveThese=["printers", "spools", "spoolManufacturers", "jobs"])
class _SimplePrinterDB:
	def __init__(self, backingFile):
		self.printers = {};
		self.spools = {};
		self.spoolManufacturers = {};
		self.jobs = {};
		self.backingFile = backingFile; # Where The DB Will Be saved
	def getPrinter(self, printerId):
		if printerId in self.printers:
			return self.printers[printerId];
		return None;
	def listPrinters(self):
		return [i for i in self.printers];
	def deletePrinter(self, printerId):
		del self.printers[printerId];
		return True;
	def newPrinter(self):
		printerId = "printer-" + str(uuid());
		self.printers[printerId] = PrinterObject();
		return printerId;

	def getSpool(self, spoolId):
		if spoolId in self.spools:
			return self.spools[spoolId];
		return None;
	def listSpools(self):
		return [i for i in self.spools];
	def deleteSpool(self, spoolId):
		del self.spools[spoolId];
		return True;

	# def getSpoolManufacturer(self, mfrId):
	# 	if mfrId in self.spoolManufacturers:
	# 		return self.spoolManufacturers[mfrId];
	# 	return None;
	# def listSpoolManufacturers(self):
	# 	return [i for i in self.spoolManufacturers];
	# def deleteSpoolManufacturer(self, mfrId):
	# 	del self.spoolManufacturers[mfrId];
	# 	return True;

	def newJob(self):
		jobId = "job-" + str(uuid());
		self.jobs[jobId] = JobObject();
		return jobId;
	def getJob(self, jobId):
		if jobId in self.jobs:
			return self.jobs[jobId];
		return None;
	def listJobs(self):
		return [i for i in self.jobs];
	def deleteJob(self, jobId):
		del self.jobs[jobId];
		return True;
	def save(self):
		f = open(self.backingFile, "w");
		f.write(json.dumps(toJsonMap(self)));
		f.close();
	@staticmethod
	def create(backingFile):
		try:
			f = open(self.backingFile, "r");
			o = fromJsonMap(json.loads(f.read()));
			f.close();
			if isinstance(o, _SimplePrinterDB):
				o.backingFile = backingFile;
				return o;
		except IOError:
			return _SimplePrinterDB(backingFile);
		return _SimplePrinterDB(backingFile);


_private_db = create("SimpleDB.json");

def getDataBase():
	return _private_db;

@JsonType(saveThese=["name", "spoolId", "printBedPlaneRange", "printHeadRange", "commProtocol", "currentJobId"])
class PrinterObject:
	def __init__(self):
		self.name = "";
		self.spoolId = None;
		self.printBedPlaneRange = [vec(0,0,0).asFloat(), vec(20,20,0).asFloat()];
		self.printHeadRange = [vec(0,0,0).asFloat(), vec(200,200,200)].asFloat();
		self.commProtocol = None;
		self.currentJobId = None;
		#Theread Instnace for Currently running job
		self.threadInfo = None;
	def getSpool(self):
		global _private_db;
		return _private_db.getSpool(self.spoolId);
	def getCurrentJob(self):
		global _private_db;
		return _private_db.getJob(self.currentJobId);
	# @staticmethod
	# def fromJson(jsonNode):
	# 	ret = PrinterObject(printerId=mapPath(jsonNode, "id"));
	# 	ret.name = mapPath(jsonNode, "name");
	# 	ret.spoolId = mapPath(jsonNode, "spoolId");
	# 	ret.printBedPlaneRange = fromJsonMap(mapPath(jsonNode, "printBedPlaneRange"));
	# 	ret.printHeadRange = fromJsonMap(mapPath(jsonNode, "printHeadRange"));
	# 	ret.commProtocol = fromJsonMap(mapPath(jsonNode, "commProtocol"));
	# 	ret.currentJobId = mapPath(jsonNode, "currentJobId");
	# 	return ret;
	# def toJson(self):
	# 	jsonNode = {};
	# 	jsonNode["name"] = self.name;
	# 	jsonNode["spoolId"] = self.spoolId;
	# 	jsonNode["printBedPlaneRange"] = toJsonMap(self.printBedPlaneRange);
	# 	jsonNode["printHeadRange"] = toJsonMap(self.printHeadRange);
	# 	jsonNode["commProtocol"] = toJsonMap(self.commProtocol);
	# 	jsonNode["currentJobId"] = self.currentJobId;

@JsonType(saveThese=["name", "bedTemp", "extruderTemp", "color", "amountLeft", "amountUsed", "diameter", "material"])
class SpoolObject:
	def __init__(self):
		self.name = "";
		self.bedTemp = 0;
		self.extruderTemp = 0;
		self.color = "";
		self.amountLeft = 0;
		self.amountUsed = 0;
		self.diameter = 0.0;
		self.material = "ABS";


@JsonType(saveThese=["name", "gcodeFilePath", "printerId", "progress", "estimatedTime", "startedTime", "fileOffset", "logfile", "state"])
class JobObject:
	def __init__(self):
		self.name = "";
		self.gcodeFilePath = "";
		self.printerId = None;
		self.progress = 0.0; # 0.0-1.0
		self.estimatedTime = 0.0; # In Seconds;
		self.startedTime = None; # Time Stamp ?
		self.fileOffset = 0; # Current Spot in file
		self.logfile = "log-" + str(uuid()) + ".txt";
		self.state = "New"; # "New", "Ready", "Stopped", "Paused", "Running", "Waiting", "Finished", etc.
	def getPrinter(self):
		global _private_db;
		_private_db.getPrinter(self.printerId);



@OnShutdown
def libPrinterObjectsShutdown():
	global _private_db.save();

		