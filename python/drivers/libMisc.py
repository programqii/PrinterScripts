from lib3dPrinter import MarlinPrinterProtocol
from libComms import ComPortWrapper, MockComPortWrapper

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