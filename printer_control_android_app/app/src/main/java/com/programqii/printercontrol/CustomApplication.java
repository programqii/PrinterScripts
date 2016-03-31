package com.programqii.printercontrol;

import android.app.Application;

import com.programqii.printercontrol.services.GcodePrinterService;

import okhttp3.OkHttpClient;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class CustomApplication extends Application {
	private GcodePrinterService gcodePrinterService;

	@Override
	public void onCreate() {
		super.onCreate();
		OkHttpClient okHttpClient = new OkHttpClient.Builder().build();
		Retrofit retrofit = new Retrofit.Builder()
			.baseUrl("http://MyServersUrl")
			.client(okHttpClient)
			.addConverterFactory(GsonConverterFactory.create())
			.build();
		gcodePrinterService = retrofit.create(GcodePrinterService.class);
	}

	public GcodePrinterService getGcodePrinterService() {
		return gcodePrinterService;
	}
}
