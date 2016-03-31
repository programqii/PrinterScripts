package com.programqii.printercontrol.services;

public class GcodeCommandConstants {
	public static final String MOVE = "G1";
	public static final String GET_END_STOPS = "M119";
	public static final String SET_RELATIVE_COORDINATES = "G91";
	public static final String SET_ABSOLUTE_UNITS = "G90";
	public static final String GET_CAPABILITIES = "M115";
	public static final String HOME ="G28";
	public static final String SET_UNITS_TO_MM = "G21";
	public static final String SET_COORDINATES = "G92"; //Sets location to coordinates given
	public static final String GET_EXTRUDER_TEMP = "M105";
	public static final String ENABLE_ALL_STEPERS = "M17";
	public static final String DISABLE_ALL_STEPPERS = "M18";
	public static final String GET_POSITION = "M114";
}
