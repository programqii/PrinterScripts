from lib3dPrinter import MarlinPrinterProtocol, GcodeCommandBuffer
from libComms import ComPortWrapper, MockComPortWrapper
from libUtils import ArgsParse, printerFromArgs
from libLogging import buildLogger

args = ArgsParse();
logger = buildLogger("print.py")
printer = printerFromArgs(args);
logger.logInfo("Accessing Printer..");
printer.open();
logger.logInfo("Sending E-Stop..");
printer.emergencyStop();
printer.close();
logger.logInfo("Done!");



