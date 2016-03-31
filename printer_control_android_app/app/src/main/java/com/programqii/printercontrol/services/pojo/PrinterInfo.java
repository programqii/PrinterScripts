package com.programqii.printercontrol.services.pojo;

public class PrinterInfo {
	private String firmwareName;
	private String firmwareUrl;
	private String protocolVersion;
	private String machineType;
	private int extruderCount;

	public String getFirmwareName() {
		return firmwareName;
	}

	public void setFirmwareName(String firmwareName) {
		this.firmwareName = firmwareName;
	}

	public String getFirmwareUrl() {
		return firmwareUrl;
	}

	public void setFirmwareUrl(String firmwareUrl) {
		this.firmwareUrl = firmwareUrl;
	}

	public String getProtocolVersion() {
		return protocolVersion;
	}

	public void setProtocolVersion(String protocolVersion) {
		this.protocolVersion = protocolVersion;
	}

	public String getMachineType() {
		return machineType;
	}

	public void setMachineType(String machineType) {
		this.machineType = machineType;
	}

	public int getExtruderCount() {
		return extruderCount;
	}

	public void setExtruderCount(int extruderCount) {
		this.extruderCount = extruderCount;
	}
}
