from lib3dPrinter import MarlinPrinterProtocol, GcodeCommandBuffer
from libComms import ComPortWrapper, MockComPortWrapper
from libUtils import ArgsParse
from libLogging import *


def printerFromArgs(args):
	return MarlinPrinterProtocol(ComPortWrapper(
		port=args.getValue("port",'/dev/ttyACM0'), 
		baud=int(args.getValue("baud", 115200)), 
		timeout=float(args.getValue("timeout", 0.5)) 
		));
# Sends G-Code to Printer

args = ArgsParse();
logger = ConsoleLoggerFactory().buildLogger("print.py")

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
		if not printer.sendCmd(i["cmd"]):
			logger.logError("Running Emergency Stop!!!!")
			printer.emergencyStop();
			printer.close();
			logger.logError("Exiting On Line: " + str(i["line"]));
			exit(1);
	if prevPercent != int((100*curLine) / amount):
		prevPercent = int((100*curLine) / amount);
		logger.logInfo("Print Progress: " + str(prevPercent) + "%% Complete");
	curLine +=1
p.close();



