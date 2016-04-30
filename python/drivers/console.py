from lib3dPrinter import MarlinPrinterProtocol, GcodeCommandBuffer
from libComms import ComPortWrapper, MockComPortWrapper
from libUtils import ArgsParse, printerFromArgs, rawUserInput
from libLogging import buildLogger

args = ArgsParse();
printer = printerFromArgs(args);
printer.open();
trueish = ['yes', 'true', '1', 't', 'y', 'on'];
falseish = ['no', 'false', '0', 'f', 'n', 'off'];

running = True;

while running:
	cmdRaw = rawUserInput("> ")
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
				printer.sendCmd("G91")
			if temp in falseish:
				printer.sendCmd("G90")
	elif cmd == "pos":
		printer.sendCmd("M114");
	elif cmd == "motors":
		v = cmdRaw.split(" ");
		if len(v) > 1:
			temp = v[1].lower();
			if temp in trueish:
				printer.sendCmd("M17")
			if temp in falseish:
				printer.sendCmd("M18")
	elif cmd == "info":
		printer.sendCmd("M115");
	elif cmd == "endstops":
		printer.sendCmd("M119");
	elif cmd == "status":
		printer.sendCmd("M115"); #Capabilities string
		printer.sendCmd("M114"); #Position
		printer.sendCmd("M119"); #End stops
		printer.sendCmd("M105"); # Current Temp
	elif cmd == "stop":
		printer.sendCmd("M18"); #stop Motors
		printer.sendCmd("M190 S0"); #Set bed temp to 0
		printer.sendCmd("M104 S0"); #Set Nozzle temp to 0
	elif cmd == "home":
		printer.sendCmd("G28")
	else:
		printer.sendCmd(cmdRaw);


printer.close();



