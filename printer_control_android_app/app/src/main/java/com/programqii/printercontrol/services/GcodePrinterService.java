package com.programqii.printercontrol.services;

import com.programqii.printercontrol.services.pojo.CommandRequest;
import com.programqii.printercontrol.services.pojo.CommandResponse;

import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.POST;

public interface GcodePrinterService {
	@POST("sendRawCommand")
	public Call<CommandResponse> sendRawCommand(@Body CommandRequest request);

}
