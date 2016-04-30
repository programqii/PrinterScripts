
import time
import datetime
class TeeLoggerFactory:
	def __init__(self, factories=[]):
		self.factories = factories;
	def buildLogger(self, tag):
		return TeeLogger(loggers=[x.buildLogger(tag) for x in self.factories]);
class TeeLogger:
	def __init__(self, loggers=[]):
		self.loggers = loggers;
	def log(self, message, level=""):
		for i in self.loggers:
			i.log(message, level);
	def logError(self, message):
		self.log(message=message, level="Error");
	def logInfo(self, message):
		self.log(message=message, level="Info");
	def logVerbose(self, message):
		self.log(message=message, level="Verbose");
# globalLoggerFactory = LoggerFactory();
# def buildLogger(tag):
# 	global globalLoggerFactory;
# 	return globalLoggerFactory.buildLogger(tag);
class ConsoleLoggerFactory:
	def __init__(self):
		self.mLogger = self.buildLogger("ConsoleLoggerFactory");
		self.mLogger.logInfo("");
		self.mLogger.logInfo("----------- Init ConsoleLoggerFactory --------");
	def buildLogger(self, tag):
		return ConsoleLogger(self, tag);
class FileLoggerFactory:
	def __init__(self, fileName="logFile.txt"):
		self.mLogFileName = fileName;
		self.mFileHandle = open(self.mLogFileName, "a");
		self.mLogger = self.buildLogger("FileLoggerFactory");
		self.mLogger.logInfo("");
		self.mLogger.logInfo("----------- Init FileLoggerFactory --------");
	def buildLogger(self, tag):
		return FileLogger(tag, self.mFileHandle);
	def __del__(self):
		if self.mFileHandle != None:
			self.mFileHandle.flush();
			self.mFileHandle.close();
class NullLoggerFactory:
	def __init__(self):
		return;
	def buildLogger(self, tag):
		return NullLogger();

class ConsoleLogger: #Prints Messages to Stdout
	def __init__(self, tag, logFileHandle=None):
		self.tag = tag;
		self.logFileHandle = logFileHandle;
	def log(self, message, level=""):
		if message == None:
			return;
		for msg in message.split("\n"):
			logEntry = "{timestamp} [{level}] {tag}: {message}".format(
				message=msg,
				tag=self.tag,
				level=level,
				timestamp=datetime.datetime.now()
				);
			print(logEntry);
	def logError(self, message):
		self.log(message=message, level="Error");
	def logInfo(self, message):
		self.log(message=message, level="Info");
	def logVerbose(self, message):
		self.log(message=message, level="Verbose");
class FileLogger:
	def __init__(self, tag, logFileHandle=None):
		self.tag = tag;
		self.mFileHandle = logFileHandle;
	def log(self, message, level=""):
		if message == None:
			return;
		for msg in message.split("\n"):
			logEntry = "{timestamp} [{level}] {tag}: {message}".format(
				message=msg,
				tag=self.tag,
				level=level,
				timestamp=datetime.datetime.now()
				);
			if self.mFileHandle != None:
				self.mFileHandle.write(logEntry + "\n");
	def logError(self, message):
		self.log(message=message, level="Error");
	def logInfo(self, message):
		self.log(message=message, level="Info");
	def logVerbose(self, message):
		self.log(message=message, level="Verbose");
class NullLogger:
	def __init__(self):
		return;
	def log(self, message, level=""):
		return;
	def logError(self, message):
		return;
	def logInfo(self, message):
		return;
	def logVerbose(self, message):
		return;