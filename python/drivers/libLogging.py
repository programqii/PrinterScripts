

globalLoggerFactory = LoggerFactory();
def buildLogger(tag):
	global globalLoggerFactory;
	return globalLoggerFactory.buildLogger(tag);

class LoggerFactory:
	def __init__(self):
		self.mLogFileName = "logfile.txt";
		self.mFileHandle = open(self.mLogFileName, "a");
		self.mLogger = self.buildLogger("LoggerFactory");
		self.mLogger.logInfo("");
		self.mLogger.logInfo("----------- Init Logger --------");
	def buildLogger(self, tag):
		return Logger(self, tag, self.mFileHandle);
	def __del__(self):
		self.mFileHandle.flush();
		self.mFileHandle.close();
class Logger:
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
			if self.mFileHandle != None:
				self.mFileHandle.write(logEntry + "\n");
	def logError(self, message):
		self.log(message=message, level="Error");
	def logInfo(self, message):
		self.log(message=message, level="Info");
	def logVerbose(self, message):
		self.log(message=message, level="Verbose");