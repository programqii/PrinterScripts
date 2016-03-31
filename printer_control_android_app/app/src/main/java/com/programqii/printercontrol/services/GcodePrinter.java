package com.programqii.printercontrol.services;

import com.programqii.printercontrol.services.pojo.CommandRequest;
import com.programqii.printercontrol.services.pojo.CommandResponse;
import com.programqii.printercontrol.services.pojo.EndStops;
import com.programqii.printercontrol.services.pojo.PrinterInfo;

import java.io.IOException;

import retrofit2.Call;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class GcodePrinter {
	GcodePrinterService gcodePrinterService;
	public GcodePrinter(String baseUrl) {
		Retrofit retrofit = new Retrofit.Builder()
				.baseUrl(baseUrl)
				.addConverterFactory(GsonConverterFactory.create())
				.build();
		gcodePrinterService = retrofit.create(GcodePrinterService.class);
	}
	private boolean passFailRequest(Call<?> call) {
		try {
			Response<?> response = call.execute();
			if(response.code() != 200) {
				return false;
			}
			return true;
		} catch (IOException e) {
			e.printStackTrace();
			return false;
		}
	}
	public boolean setRelativeCoordinates(boolean useRelativeCoordinates){
		return passFailRequest(gcodePrinterService.sendRawCommand(new CommandRequest(useRelativeCoordinates ? "G91":"G90")));

	}
	public boolean setUnitsToMM() {
		return passFailRequest(gcodePrinterService.sendRawCommand(new CommandRequest("G21")));
	}
	public boolean home() {
		return passFailRequest(gcodePrinterService.sendRawCommand(new CommandRequest("G28")));
	}
	public boolean move(float x, float y, float z) {
		String request = "G1";
		request += x == 0 ? "": String.format(" X%.4f", x);
		request += y == 0 ? "": String.format(" Y%.4f", y);
		request += z == 0 ? "": String.format(" Z%.4f", z);
		return passFailRequest(gcodePrinterService.sendRawCommand(new CommandRequest(request)));
	}
	public PrinterInfo getCapabilities() {
		try {
			Response<CommandResponse> response = gcodePrinterService.sendRawCommand(new CommandRequest("M115")).execute();
			if(response.code() != 200) {
				return null;
			}

			//FIRMWARE_NAME:Marlin V1; Sprinter/grbl mashup for gen6 FIRMWARE_URL:http://www.mendel-parts.com PROTOCOL_VERSION:1.0 MACHINE_TYPE:FolgerTech EXTRUDER_COUNT:1

			return new PrinterInfo();
		} catch (IOException e) {
			e.printStackTrace();
			return null;
		}
	}
	public EndStops getEndStopState(){

		//--> M119 - Output Endstop status to serial port
//		<-- Reporting endstop status
//		<-- x_min: open
//		<-- x_max: TRIGGERED
//		<-- y_min: open
//		<-- y_max: TRIGGERED
//		<-- z_min: TRIGGERED
//		<-- z_max: TRIGGERED
		return null;
	}



}
