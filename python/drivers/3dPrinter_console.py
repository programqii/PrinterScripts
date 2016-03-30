import serial
import sys

class ArgsParse:
	def  __init__(self):
		self.argMap = {}
		self.flags = [];
		offset = 0;
		for i in sys.argv[1:]:
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

class PrinterProtocol:
	def __init__(self, port='/dev/ttyACM0', baud=115200, timeout=0.5):
		self.mPort = port;
		self.mBaud = baud;
		self.mTimeout = timeout;
		self.ser = None;
		self.errors = [];
	def open(self):
		self.ser = serial.Serial(self.mPort, self.mBaud, timeout=self.mTimeout);
		self.printResponse();
	def close(self):
		if self.ser != None:
			self.ser.close();
	def printResponse(self):
		while True:
			s = self.ser.readline();
			if s == '':
				break;
			print("From Printer: " + s[:-1]);
	def readUntilOkOrError(self):
		while True:
			s = self.ser.readline();
			if s.find(":") > -1:
				tag = s[:s.find(":")];
			else:
				tag = "";
			if s.lower() == "ok\n":
				return True;
			if(s != ''):
				print("From Printer: " + s[:-1]);
			if tag.lower() == "error":
				return False;
	def sendCmd(self, cmd):
		print ("App: Sending Command: " + cmd);
		self.ser.write(cmd + "\n");
		return self.readUntilOkOrError();
	def emergencyStop(self):
		self.sendCmd("M18");
		self.sendCmd("M140 S0");
		self.sendCmd("M104 S0");
		self.sendCmd("M81");
class GcodeCommandBuffer:
	def __init__(self, filePath):
		self.mLines = [];
		self.mNextCommand = 0;
		f = open(filePath);
		l = f.readline();
		lineCounter = 1;
		while l != '':
			commentPos = l.find(";");
			comment = None
			if(commentPos > -1):
				comment = l[commentPos+1:].strip();
				l = l[:commentPos];
			l = l.strip();
			if(len(l) > 0 or comment != None):
				self.mLines += [{"cmd":l, "comment":comment, "line":lineCounter}]; 
			lineCounter += 1
			l = f.readline();
		f.close();
	def nextCommand(self):
		if(nextCommand < len(self.mLines)):
			temp = self.mLines[self.mNextCommand];
			self.mNextCommand += 1;
			return temp;
		return {"cmd": "", "comment":"End of commands!!!", "line":-1};
	def percentComplete(self):
		return (1.0*self.mNextCommand) / len(self.mLines);
	def numCommandsLeft(self):
		return len(self.mLines) - self.mNextCommand;
args = ArgsParse();

baud = args.getValue("baud", 115200);
port = args.getValue("port", '/dev/ttyACM0');
print("Params: port=" + port + ", baud=" + str(baud));
p = PrinterProtocol(port=port, baud=baud, timeout=1.0);
p.open();
trueish = ['yes', 'true', '1', 't', 'y', 'on'];
falseish = ['no', 'false', '0', 'f', 'n', 'off'];
running = True;

while running:
	cmdRaw = raw_input("> ")
	cmd = cmdRaw.split(" ")[0].lower();
	if cmd == "":
		print("Nop");
	elif cmd == "help" or cmd == "?":
		print("""
Custom Commands:
	help / ? - shows this
	quit / exit / - stops console 
	relative <true/false> - use Relative Movements
	pos - show current position
	info - show printer info
	endstops - show endstop status
	motors <true/false> - turn motors on?
	home - home the printer
	status - print avaialble info to screen
	stop - Emergency stop of printer
* Note Any Non-Custom Commands will be treated as GCODE and be sent un-altered to printer
""")
	elif cmd == "exit" or cmd == "quit" or cmd == "q":
		running = False;
	elif cmd == "relative":
		v = cmdRaw.split(" ");
		if len(v) > 1:
			temp = v[1].lower();
			if temp in trueish:
				p.sendCmd("G91")
			if temp in falseish:
				p.sendCmd("G90")
	elif cmd == "pos":
		p.sendCmd("M114");
	elif cmd == "motors":
		v = cmdRaw.split(" ");
		if len(v) > 1:
			temp = v[1].lower();
			if temp in trueish:
				p.sendCmd("M17")
			if temp in falseish:
				p.sendCmd("M18")
	elif cmd == "info":
		p.sendCmd("M115");
	elif cmd == "endstops":
		p.sendCmd("M119");
	elif cmd == "status":
		p.sendCmd("M115"); #Capabilities string
		p.sendCmd("M114"); #Position
		p.sendCmd("M119"); #End stops
		p.sendCmd("M105"); # Current Temp
	elif cmd == "stop":
		p.sendCmd("M18"); #stop Motors
		p.sendCmd("M190 S0"); #Set bed temp to 0
		p.sendCmd("M104 S0"); #Set Nozzle temp to 0
	elif cmd == "home":
		p.sendCmd("G28")
	else:
		p.sendCmd(cmdRaw);


p.close();



