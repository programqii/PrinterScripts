package com.programqii.printercontrol;

import android.support.v7.app.AppCompatActivity;

import com.programqii.printercontrol.services.GcodePrinterService;

public class BaseActivity extends AppCompatActivity {
	public GcodePrinterService getGcodePrinterService() {
		return ((CustomApplication)getApplication()).getGcodePrinterService();
	}
}
