package com.programqii.printercontrol.services.pojo;

import com.google.gson.annotations.SerializedName;

public enum EndStopState {
	@SerializedName("TRIGGERED")
	TRIGGERED,
	@SerializedName("open")
	OPEN
}
