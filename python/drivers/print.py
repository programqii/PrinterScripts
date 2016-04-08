from lib3dPrinter import MarlinPrinterProtocol, GcodeCommandBuffer
from libComms import ComPortWrapper, MockComPortWrapper
from libUtils import ArgsParse, printerFromArgs
from libLogging import buildLogger

# Sends G-Code to Printer

args = ArgsParse();
logger = buildLogger("print.py")

logger.logInfo("Parsing GCODE file...")
filePath = args.getValue("file", None);
commands = GcodeCommandBuffer(filePath);
logger.logInfo("Parsing Done!");
printer = printerFromArgs(args);
logger.logInfo("Accessing Printer...")
printer.open();
logger.logInfo("Starting Print...")
prevPercent = -1;
amount = commands.numCommandsLeft();
curLine =0;
for i in commands.mLines:
	if i["comment"] != None:
		logger.logInfo("Comment From File: " + i["comment"]);
	if i["cmd"] != None and len(i["cmd"]) > 0:
		if not p.sendCmd(i["cmd"]):
			logger.logError("Running Emergency Stop!!!!")
			p.emergencyStop();
			p.close();
			logger.logError("Exiting On Line: " + str(i["line"]));
			exit(1);
	if prevPercent != int((100*curLine) / amount):
		prevPercent = int((100*curLine) / amount);
		logger.logInfo("Print Progress: " + str(prevPercent) + "%% Complete");
	curLine +=1
p.close();



