from uuid import uuid1 as uuid
from libUtils import *
from libVec import vec
from libLogging import NullLoggerFactory, FileLoggerFactory
import json
import threading, Queue
import time

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
		if jobId in self.jobs:
			del self.jobs[jobId];
			return True;
		return False;
	def save(self):
		f = open(self.backingFile, "w");
		f.write(json.dumps(toJsonMap(self)));
		f.close();
	def shutdown(self):
		# Shutdown All threads
		for p in self.printers:
			self.printers[p].shutdown();
		self.save();
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

#TODO: Put this _private_db in the Main print_server.py file if possible
_private_db = create("SimpleDB.json");

def getDataBase():
	return _private_db;
class PrinterThread(threading.Thread):
	def __init__(self, parentPrinterObject):
		self.parentPrinterObject = parentPrinterObject;
		self.shutdownRequest = threading.Event();
		self.rawCmdBufferQueue = Queue.Queue();
		self.rawCmdResult = None;
		self.job = parentPrinterObject.getCurrentJob() if self.getCurrentJob() != None else None;
		if self.job.state in ["Stopped", "Done"]:
			self.job = None;
		self._jobLock =  threading.Semaphore();
		self._runningLock =  threading.Semaphore();
		self._runningLock.acquire();
	def _getNextJobCmd(self):
		with BeginEnd(self._jobLock.acquire, self._jobLock.release) as aLock:
			job = self.job;
			if job == None or job.state != "Running":
				return None;
			cmd = job.getNextCmd();
			if cmd == None:
				job.state = "Done";
				self.job = None;
				self.parentPrinterObject.currentJobId = None;
			return cmd;
	def _runRawCommands(self):
		comm = self.parentPrinterObject.commProtocol;
		if comm == None or self.rawCmdBufferQueue.empty():
			return ;
		data = self.rawCmdBufferQueue.get();
		data["result"] = [];
		index = 0;
		while not self.shutdownRequest.isSet() and index < len(data["cmds"]):
			data["result"] += comm.sendCmd(data["cmds"][index]);
			index += 1;
		data["resultLock"].release();
	def run(self):
		comm = self.parentPrinterObject.commProtocol;
		if comm == None:
			return ;
		comm.open();
		while not self.shutdownRequest.isSet():
			self._runRawCommands();
			if not self.shutdownRequest.isSet():
				# TODO: Add Command Timing (To know how long a comand will take to run) and transformation (Ex: G-Code <0,0,0> != Printer <0,0,0> )
				cmd = self._getNextJobCmd();
				if cmd == None:
					time.sleep(0.1);
				else:
					comm.sendCmd(cmd);
		comm.close();
		self._runningLock.release();
	def runRawCommands(self, rawCommandList=[]):
		# Note: might convrt This into a Queue of Queues so that individual rawCmd Requests return once they are complete.
		data = {"cmds": rawCommandList, "resultLock": threading.Semaphore(), "result":None};
		self.rawCmdBufferQueue.put(data);
		data["resultLock"].acquire();
		data["resultLock"].acquire(); # Intentionally block this thread to have the Printer Thread Release the Semaphore Once it's finished (IE: Wait for result)
		return data["result"];
	def startJob(self): # also Doubles as "resume"
		with BeginEnd(self._jobLock.acquire, self._jobLock.release) as aLock:
			if self.job == None:
				return ;
			if self.job.state in ["Done", "Stopped"]:
				self.job = None;
				return ;
			if self.job.state in ["New", "Running", "Paused"]:
				self.job.state = "Running";
				self.job.log("Changing Job State: " + self.job.state + " -> Running");
				return True;
			else:
				self.job.log("Job cannot Be started/Resumed, State: " + str(job.state));
				return False;
	def stopJob(self):
		with BeginEnd(self._jobLock.acquire, self._jobLock.release) as aLock:
			if self.job != None:
				self.job.log("Job Stopped");
				self.job.state = "Stopped";
				if self.job.getPrinter() != None:
					self.job.getPrinter().currentJobId = None;
				self.job = None;
				return True;
			else:
				return False;
	def pauseJob(self):
		with BeginEnd(self._jobLock.acquire, self._jobLock.release) as aLock:
			job = self.job;
			if job != None and job.state in ["Running", "Paused", "New"];
				self.job.state = "Paused";
				job.log("Job Paused");
				return True;
			else:
				return False;
	def setJob(self, job):
		with BeginEnd(self._jobLock.acquire, self._jobLock.release) as aLock:
			if job == self.job:
				return ;
			if self.job != None and self.job.state in ["Running", "Paused", "Waiting"]:
				self.job.state = "Stopped";
				self.job = job;
				self.comm.setLoggerFactory(self.job.getLoggerFactroy());

	def shutdown(self):
		self.shutdownRequest.set();
		self._runningLock.acquire();
		self._runningLock.release();


@JsonType(saveThese=["name", "spoolId", "printBedPlaneRange", "printHeadRange", "commProtocol", "currentJobId"])
class PrinterObject:
	def __init__(self):
		self.name = "";
		self.spoolId = None;
		self.printBedPlaneRange = [vec(0,0,0).asFloat(), vec(20,20,0).asFloat()];
		self.printHeadRange = [vec(0,0,0).asFloat(), vec(200,200,200)].asFloat();
		self.commProtocol = None;
		self.currentJobId = None;
		#Thread Instance for Currently running job
		self.threadInfo = None;
	def getSpool(self):
		global _private_db;
		return _private_db.getSpool(self.spoolId);
	def getCurrentJob(self):
		global _private_db;
		return _private_db.getJob(self.currentJobId);
	def _getThread(self):
		if self.threadInfo == None:
			self.threadInfo = PrinterThread(self);
	def startJob(self):
		job = self.getCurrentJob();
		if job != None and job.state in ["New"]:
			self._getThread().setJob(self.getCurrentJob());
		return self._getThread().startJob();
	def stopJob(self):
		return self._getThread().stopJob();
	def pauseJob(self):
		return self._getThread().pauseJob();
	def runRawCommands(self, commandList=[]):
		return self._getThread().runRawCommands(commandList);
	def shutdown(self):
		if self.threadInfo != None:
			self.threadInfo.shutdown();
			self.threadInfo = None;
			#Clear Job (Just in case)
			self.currentJobId = None;
		return ;

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


@JsonType(saveThese=["name", "gcodeFilePath", "printerId", "progress", "estimatedTime", "startedTime", "fileOffset", "logfile", "state", "linesProcessed"])
class JobObject:
	def __init__(self):
		self.name = "";
		self.gcodeFilePath = None;
		self.printerId = None;
		self.progress = 0.0; # 0.0-1.0
		self.estimatedTime = 0.0; # In Seconds;
		self.startedTime = None; # Time Stamp ?
		self.fileOffset = 0; # Current Spot in file
		self.logfile = "log-" + str(uuid()) + ".txt";
		self.state = "New"; # "New", "Stopped", "Paused", "Running", "Waiting", "Done", etc.
		self._loggerFactory = None;
		self._gcodeFileRef = None;
		self._fileSize = 0;
		self.linesProcessed = 0;
		self._jobLogger = None;
	def log(self, text):
		if self._jobLogger == None:
			self._jobLogger = getLoggerFactroy().buildLogger("JobObject");
		self._jobLogger.log(text)
	def getLoggerFactroy(self):
		if self._loggerFactory != None:
			return self._loggerFactory;
		if self.logfile != None:
			self._loggerFactory = FileLoggerFactory(self.logfile);
		else:
			self._loggerFactory = NullLoggerFactory();
	def getPrinter(self):
		global _private_db;
		_private_db.getPrinter(self.printerId);
	def getNextCommand(self):
		if self.gcodeFilePath == None:
			return None;
		if self._gcodeFileRef == None:
			self._gcodeFileRef = open(self.gcodeFilePath, "r");
			self._gcodeFileRef.seek(0, 2);
			self._fileSize = self._gcodeFileRef.tell();
			self._gcodeFileRef.seek(self.fileOffset);
		l = self._gcodeFileRef.readLine();
		while l != '':
			commentPos = l.find(";");
			comment = None
			if(commentPos > -1):
				comment = l[commentPos+1:].strip();
				l = l[:commentPos];
			l = l.strip();
			if(len(l) > 0 or comment != None):
				#self.mLines += [{"cmd":l, "comment":comment, "line":lineCounter}]; 
				self.fileOffset = f.tell();
				return l;
			self.linesProcessed += 1
			l = f.readline();
		return None;
	def shutdown():
		return ;

@OnShutdown
def libPrinterObjectsShutdown():
	global _private_db
	_private_db.shutdown();

		