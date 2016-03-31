package com.programqii.printercontrol.services.pojo;

public class EndStops {
	private EndStopState xMin;
	private EndStopState xMax;
	private EndStopState yMin;
	private EndStopState yMax;
	private EndStopState zMin;
	private EndStopState zMax;

	public EndStopState getXMin() {
		return xMin;
	}

	public void setXMin(EndStopState xMin) {
		this.xMin = xMin;
	}

	public EndStopState getXMax() {
		return xMax;
	}

	public void setXMax(EndStopState xMax) {
		this.xMax = xMax;
	}

	public EndStopState getYMin() {
		return yMin;
	}

	public void setYMin(EndStopState yMin) {
		this.yMin = yMin;
	}

	public EndStopState getYMax() {
		return yMax;
	}

	public void setYMax(EndStopState yMax) {
		this.yMax = yMax;
	}

	public EndStopState getZMin() {
		return zMin;
	}

	public void setZMin(EndStopState zMin) {
		this.zMin = zMin;
	}

	public EndStopState getZMax() {
		return zMax;
	}

	public void setZMax(EndStopState zMax) {
		this.zMax = zMax;
	}
}
