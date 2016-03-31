package com.programqii.printercontrol.services.pojo;

import android.support.annotation.Nullable;

public class CommandRequest {
	private String command;
	public CommandRequest(@Nullable String command) {
		this.command = command;
	}
	@Nullable
	public String getCommand() {
		return command;
	}

	public void setCommand(String command) {
		this.command = command;
	}
}
