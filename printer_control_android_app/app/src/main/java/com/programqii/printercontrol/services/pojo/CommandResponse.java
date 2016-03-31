package com.programqii.printercontrol.services.pojo;


import android.support.annotation.NonNull;

import java.util.LinkedList;
import java.util.List;

public class CommandResponse {
	private List<String> data;

	@NonNull
	public List<String> getData() {
		if(data == null) {
			data = new LinkedList<>();
		}
		return data;
	}
}
